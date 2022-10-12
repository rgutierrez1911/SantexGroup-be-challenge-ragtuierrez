from typing import List
from core.general.schemas import OrmModel
from core.general.schemas import Pager

class NewUser(OrmModel):
  user_name: str
  first_name: str
  last_name: str
  id_jefatura: int =1 
  id_viceprecidencia: int = 1
  id_gerencia: int= 1
  id_cargo: int =1 
  mail: str
  password: str


class DetailUserPermitions(OrmModel):
  id_usuario_grupo: int
  id_grupo: int
  id_grupo_permiso: int
  id_permiso: int
  name: str
  
  
  
class BaseDetailUserData(OrmModel):
  name: str = None
  mail: str = None
  id_colaborador: int = None
  id_jefatura: int = None
  id_viceprecidencia: int = None
  id_gerencia: int = None
  id_cargo: int = None
  gerencia: str = None
  jefatura: str = None
  viceprecidencia: str = None
  cargo: str = None

  

class DetailUserData(BaseDetailUserData):

  user_permitions: List[DetailUserPermitions] = []


class UsuariosRowDb(OrmModel):
  name: str = None
  mail: str = None
  id_colaborador: int = None
  id_jefatura: int = None
  id_viceprecidencia: int = None
  id_gerencia: int = None
  id_cargo: int = None
  gerencia: str = None
  jefatura: str = None
  viceprecidencia: str = None
  cargo: str = None


class ResponseUsuariosListDb(OrmModel):
  usuarios: List[UsuariosRowDb] = []


class UserPermitionsDb(OrmModel):
  permitions: List[str] = []
  

class DetailUserDataPager(Pager):
  data: List[BaseDetailUserData] = []
