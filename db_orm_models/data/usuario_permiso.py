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
  ForeignKey,
  Sequence
)
from db_orm_models.data.common import NamedCommonFields

from datetime import datetime
from core.extensions import base

import enum


class UsuarioPermiso( base, NamedCommonFields ):
  __tablename__ = "tm_usuario_permiso"
  __table_args__ = {'comment': 'Tabla de datos de  usuario_permiso',}
  
  id_usuario =Column(Integer , ForeignKey("tm_usuario.id") , nullable=True ,comment = "Id de  del usuario relacionado")
  id_permiso =Column(Integer , ForeignKey("tm_permiso.id") , nullable=True ,comment = "Id del permiso relacionado")
  