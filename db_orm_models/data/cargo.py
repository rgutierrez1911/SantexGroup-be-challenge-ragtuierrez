# write you database models in this file

from sqlalchemy import (
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




class Cargo( base, NamedCommonFields ):
  __tablename__ = "ts_cargo"
  __table_args__ = {'comment': 'Tabla de datos de cargo'}
  

  jefatura = Column(Boolean, nullable=True, server_default="false")
  gerencia = Column(Boolean, nullable=True, server_default="false")
  viceprecidencia = Column(Boolean, nullable=True, server_default="false")
  



