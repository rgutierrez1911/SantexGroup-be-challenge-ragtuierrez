# write you database models in this file
from db_orm_models.data.common import NamedCommonFields
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

from datetime import datetime
from core.extensions import base

import enum


class Permiso( base, NamedCommonFields ):
    __tablename__ = "tm_permiso"
    __table_args__ = {'comment': 'Tabla de datos de  permiso',}
   
    descripcion = Column(String(256), nullable=True)

