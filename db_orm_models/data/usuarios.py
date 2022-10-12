# write you database models in this file

from core.dbsetup import (
  Column,
  BigInteger,
  
  
  String,
  Integer,
  ForeignKey,
  Boolean,
  Float,
  TIMESTAMP,
  Enum,
  Identity
)
from uuid import uuid4
from datetime import datetime

from core.config import SECRET_KEY
from bcrypt import hashpw, gensalt, checkpw

from sqlalchemy.orm import column_property, join
from sqlalchemy import and_
from sqlalchemy.orm import Session
from db_orm_models.data.common import CommonFields
from core.extensions import base


class Usuario( base, CommonFields ):
  __tablename__ = "tm_usuario"
  __table_args__ = {
      'comment': 'En esta tabla de usuarios registrados',
  }

  
  name = Column(String(256), nullable=False, unique=True)
  mail = Column(String(256), nullable=False)
  hash_password = Column(String(512), nullable=True)
  state = Column(String(2), nullable=True)
  try_number = Column(Integer, nullable=True, server_default="0", default=0)
  access_type = Column(String(16), nullable=True, comment="tipo de acceso del usuario")
  id_colaborador = Column(Integer, ForeignKey("tm_colaborador.id"), nullable=True)
  

  @property
  def password(self):
    raise AttributeError('password: solo funcion de escritura')

  @password.setter
  def password(self, password: str):
    # encrypt_password = flask.current_app.config['ENCRYPT_PASSWORD']
    salt = gensalt()
    u8_password = password.encode("utf-8")
    hashed = hashpw(password=u8_password, salt=salt).decode("utf-8")
    self.hash_password = hashed

    ## tamanio hashed password[60] + hash[29] = 89
  @classmethod
  def check_password(cls, password:str="" , hashed_passwd:str=None):
    if hashed_passwd ==None:
      return checkpw(password=password.encode()  ,hashed_password= cls.hash_password.encode()) 
    else :
      return checkpw(password=password.encode()  ,hashed_password= hashed_passwd.encode())     


  def add_initial_data(self , db:Session=None):
    
    from core.dbsetup import (Usuario,
                              Cargo,
                              Viceprecidencia,
                              Jefatura,
                              Gerencia,
                              Colaborador)
    from db_orm_models.data.initial_data.base_users import (new_cargo,
                                                  new_vp,
                                                  new_gerencia,
                                                  new_jefatura,
                                                  new_colaborador,
                                                  new_usuario)
    
    
    from core.extensions import yield_session
    
    db_session = yield_session()
    db = next(db_session)
    
    db_vp = Viceprecidencia(**new_vp)
    db_cargo = Cargo(**new_cargo)

    db.add(db_vp)
    db.add(db_cargo)
    db.flush()
    
    new_gerencia["id_viceprecidencia"] = db_vp.id
    db_gerencia = Gerencia(**new_gerencia)
    db.add(db_gerencia)
    db.flush()
    
    new_jefatura["id_gerencia"] = db_gerencia.id
    new_jefatura["id_viceprecidencia"] = db_vp.id
    db_jefatura = Jefatura(**new_jefatura)
    db.add(db_jefatura)
    db.flush()
    
    new_colaborador["id_jefatura"] = db_jefatura.id
    new_colaborador["id_viceprecidencia"] = db_vp.id
    new_colaborador["id_gerencia"] = db_gerencia.id
    new_colaborador["id_cargo"] = None

    db_colaborador = Colaborador(**new_colaborador)

    db.add(db_colaborador)
    db.flush()

    new_usuario["id_colaborador"] = db_colaborador.id

    db_usuario=Usuario(**new_usuario)
    db.add(db_usuario)
    db.flush()
    db.commit()