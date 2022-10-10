
from fastapi import Depends, Query


from jose import JWTError
from datetime import timedelta
from fastapi import APIRouter
from datetime import datetime
# from app.jaeger_service.manager import decorate_function_span
from core.extensions import yield_session, Session
from dependencies.user_dependencies import user_token_data

from .tokens import create_access_token, create_refresh_token, decode_refresh_jwt

from .exceptions import token_type_refresh_exception
from core.factories import settings
from .factories import get_auth_service
from .schema import TokenResponse, RequestFormAccess, RefreshToken, RevalidateToken, UsuarioData, UserAccess


router = APIRouter()

tags = ["AUTH"]
router.tags = tags


@router.post("/token", response_model=TokenResponse, tags=tags)
async def login_for_access_token(
    form_data: RequestFormAccess = Depends(),
    db: Session = Depends(yield_session)
):
    auth_service = get_auth_service(auth_type=form_data.grant_type.value)

    user_auth = auth_service.authenticate_user_db(
        db=db,
        username=form_data.username,
        password=form_data.password,
    )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": user_auth.name,
            "id_user": user_auth.id,
            "generated": str(datetime.now())
        },
        expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(
        data={"sub": user_auth.name,
              "id_user": user_auth.id,
              "generated": str(datetime.now())
              }, expires_delta=refresh_token_expires
    )

    token_data = {"access_token": access_token,
                  "refresh_token": refresh_token,
                  "token_type": "bearer",
                  **user_auth.dict()}

    return token_data


@router.post("/get-token", response_model=RevalidateToken, tags=tags)
async def get_new_access_token(token: RefreshToken):
    try:

        username, id_user = decode_refresh_jwt(
            token=token.token, enforced_token_type="refresh")
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={
                "sub": username,
                "id_user": id_user,
                "generated": str(datetime.now())
            },
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except JWTError:
        raise token_type_refresh_exception


@router.get("/users/me/", response_model=UsuarioData)
# @decorate_function_span(optional_name= "read_users_me")
async def read_users_me(
    session_user: UserAccess = user_token_data(),
    name: str = Query(...),
):

    return {
        "id": session_user.user.id,
        "name": session_user.user.name
    }
