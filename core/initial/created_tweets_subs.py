from core.extensions import Session, session_decorator
from core.dbsetup import (Usuario,
                          Cargo,
                          Viceprecidencia,
                          Jefatura,
                          Gerencia, Colaborador,
                          Permiso,
                          Grupo,
                          GrupoPermiso,
                          UsuarioGrupo,
                          UserSubscribers,
                          Tweets)
from db_orm_models.data.initial_data.base_users import *
from db_orm_models.data.initial_data.base_permitions import permisos, grupo_admin, grupos_product


@session_decorator
def add_initial_data_tweets(db: Session = None):

  first_subscription = UserSubscribers(
      user_id=1,
      subscriber_id=2,
  )

  second_subscription = UserSubscribers(
      user_id=2,
      subscriber_id=1,
  )

  db.add(first_subscription)
  db.add(second_subscription)

  db.flush()
  db.commit()
