from enum import Enum
from typing import Optional
from pydantic import validator
from typing import List
from fastapi.param_functions import Form
from core.general.schemas import OrmModel
from sqlalchemy.orm import Session
class Token(OrmModel):
    access_token: str
    token_type: str




class TokenData(OrmModel):
    username: Optional[str] = None


class User(OrmModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

class UsuarioData(OrmModel):
    id:int
    name:str

class UserInDB(User):
    hashed_password: str

class GrantType(str,Enum):
    ldap="ldap"
    password="password"

class RequestFormAccess:

    def __init__(
        self,
        grant_type: GrantType = Form(None),
        username: str = Form(...),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
class PermisosUsuarioLocal(OrmModel):
    permisos_usuario:List[str]= []
    permisos_grupo:List[str]= []


class BaseUser (OrmModel):
    id:int=None
    name:str=None
    mail:str=None
    

    id_jefatura:int=None
    id_gerencia:int=None
    id_viceprecidencia:int=None
    id_cargo :int = None

    first_name:str = None
    last_name:str = None


    jefatura:str=None
    gerencia:str=None
    viceprecidencia:str=None
    cargo:str = None
    
    complete_name:str = None
    permitions:PermisosUsuarioLocal=None

class UsuarioDB(BaseUser):

    hash_password:str=None



    @validator('complete_name' , always=True)
    def complete_name_generate(cls, v, values, **kwargs):
        return f'{values["first_name"]} {values["last_name"]}'

class TokenResponse(BaseUser):
    access_token: str
    refresh_token :str
    token_type: str
    


class RevalidateToken(OrmModel):
    access_token:str
    token_type:str

class RefreshToken(OrmModel):
    token:str

class TokenDataService(TokenData):
    id_user :int
    disabled :bool =False


class DbUser(OrmModel):
    id:int 
    name:str
    mail:str
    state:str
    access_type:str
    active:bool
    full_name:str



class UserAccess:

    def __init__(self, current_user: DbUser, session: Session , permitions:List[str] = None) -> None:
        self.permitions = permitions or []
        self.user = current_user
        self.db = session
        self.selected_permition = None
        
