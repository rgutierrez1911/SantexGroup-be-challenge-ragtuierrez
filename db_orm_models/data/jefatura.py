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

from core.extensions import base


class Jefatura ( base, NamedCommonFields ):
    __tablename__ = "ts_jefatura"
    __table_args__ = {
        'comment': 'Tabla de datos de jefatura',
    }
       
    
    id_gerencia = Column(Integer , ForeignKey("ts_gerencia.id") , nullable=True ,comment = "Id de la gerencia de la jefatura ")
    id_viceprecidencia = Column(Integer, ForeignKey("ts_viceprecidencia.id"), nullable=True)
    
