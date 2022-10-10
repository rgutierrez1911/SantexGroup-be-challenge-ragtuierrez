# write you database models in this file
from db_orm_models.data.common import NamedCommonFields
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
from datetime import datetime
from core.extensions import base

class Grupo( base, NamedCommonFields ):
    __tablename__ = "tm_grupo"
    __table_args__ = {'comment': 'Tabla de datos de grupo',}


   