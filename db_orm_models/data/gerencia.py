# write you database models in this file

from db_orm_models.data.common import  NamedCommonFields
from sqlalchemy  import (
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

from core.extensions import base





class Gerencia( base, NamedCommonFields ):
  __tablename__ = "ts_gerencia"
  __table_args__ = { 'comment': 'Tabla de datos de gerencia',}
  
  tipo_gerencia = Column(String(128), nullable=True)
  id_viceprecidencia = Column(Integer , ForeignKey("ts_viceprecidencia.id") , nullable=True ,comment = "Id de la viceprecidencia de la gerencia ")

