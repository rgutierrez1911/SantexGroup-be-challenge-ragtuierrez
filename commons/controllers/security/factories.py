from abc import ABC, abstractclassmethod, abstractmethod
from sqlalchemy.orm import Session

from .schema import UsuarioDB

from db_orm_models.data.usuarios import Usuario
from commons.storage import get_user_permitions, search_user_db
from .exceptions import credentials_exception


class ApiAuthBase(ABC):

  @abstractclassmethod
  def authenticate_user_db(cls, *args, **kwargs) -> UsuarioDB: ...


class DbWebAuth(ApiAuthBase):
  @classmethod
  def authenticate_user_db(
      cls,
      db: Session,
      username: str,
      password: str,
  ) -> UsuarioDB:

    user = search_user_db(db=db, username=username)

    if not cls.check_password(user=user, password=password):
        raise credentials_exception

    permitions = get_user_permitions(session=db,
                                      id_usuario=user.id)

    formatted_permitions = {"permisos_usuario": permitions["user_permitions"],
                            "permisos_grupo": permitions["group_permitions"]}

    return UsuarioDB(**user._asdict(), permitions=formatted_permitions)

  @classmethod
  def check_password(cls, user: Usuario, password: str) -> bool:

    is_valid_password = Usuario.check_password(password=password,
                                                hashed_passwd=user.hash_password)
    return is_valid_password


auth_service = {
    "password": DbWebAuth,
}


def get_auth_service(auth_type: str = "password") -> ApiAuthBase:
    current_auth = auth_service[auth_type]

    return current_auth
