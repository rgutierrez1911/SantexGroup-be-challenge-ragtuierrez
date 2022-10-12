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




class Viceprecidencia( base, NamedCommonFields ):
  __tablename__ = "ts_viceprecidencia"
  __table_args__ = {'comment': 'Tabla de datos de viceprecidencia',}
