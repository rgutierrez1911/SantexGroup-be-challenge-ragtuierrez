
from typing import Tuple
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from db_orm_models.data.colaborador import Colaborador
from core.extensions import Session, yield_session
from fastapi import Depends, HTTPException , WebSocket
from urllib import parse

from jose import JWTError, jwt
from calendar import timegm
from datetime import datetime

from core.config import (ALGORITHM,
                         SECRET_KEY,)

from core.dbsetup import Usuario , Colaborador
from commons.types import UserSession
from core.general.schemas import DbUser ,UserAccess
from core.constants import token_path

from core.exceptions.auth import (
    credentials_exception,
    token_type_refresh_exception,
    type_exception,
    invalid_jwt_token)
from http.cookies import SimpleCookie
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_db(token: str, id_user: int , session:Session)->DbUser:

    fields = [
        Usuario.id,
        Usuario.name,
        Usuario.mail,
        Usuario.state,
        Usuario.access_type,
        Usuario.active,
        (Colaborador.name + " " + Colaborador.last_name).label("full_name")
    ]

    
    usuario_actual = session.query(
        Usuario
    ).join(
        Colaborador , Colaborador.id == Usuario.id_colaborador
    ).filter(
        Usuario.id == id_user,
        Usuario.visible == True,
        Usuario.active == True
    ).with_entities(
        *fields
    ).first()
    

    if usuario_actual:
        db_user = DbUser.from_orm(usuario_actual)
        db_user.token = token
        return db_user
    else:
        raise credentials_exception
    
def validate_expired(exp: int, leeway:int=0 , detail:str = "REFRESH-REQUIRED"):
    now = timegm(datetime.utcnow().utctimetuple())
    if exp < (now - leeway):
        raise HTTPException(status_code=412,
                            detail=detail,
                            headers={"WWW-Authenticate": "Bearer"}, )


def decode_token(token: str)->Tuple[dict , str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        username: str = payload.get("sub")
        token_type: str = payload.get("type", None)
        id_user: str = payload.get("id_user", None)
        exp = payload.get("exp")

        if username is None:
            raise credentials_exception
        if token_type != "access":
            raise token_type_refresh_exception
        if token_type == None:
            raise type_exception
        validate_expired(exp=exp)

        return payload, id_user

    except JWTError:
        raise invalid_jwt_token



async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session :Session= Depends(yield_session),
)->UserSession:
 
    payload, id_user = decode_token(token=token)
    user = get_user_db(token=token, id_user=id_user , session=session)
    return user , session





async def get_current_active_user(
    complete: UserSession= Depends(get_current_user)
) -> UserAccess:
    current_user, session = complete
    if not current_user.active:
        raise HTTPException(status_code=400, detail="inactive user")
    user_access=UserAccess(current_user= current_user , session=session)
    return user_access


async def get_current_user_ws(
    
    ws : WebSocket
):
    token :str= ws.query_params.get("auth")
    # cookie = SimpleCookie()
    # cookie.load(x_authorization)
    # cookie = { key : morsel.value for key , morsel in cookie.items()}
    
    # token = cookie['X-Authorization'].replace("%20" , " ")
    # token = token.split("Bearer ")[-1]
    
    
    
    db = yield_session()
    session: Session = next(db)
    payload, id_user = decode_token(token=token)
    
    user = get_user_db(token=token, id_user=id_user , session=session)
    return user  ,ws
    