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
from db_orm_models.data.common import  NamedCommonFields
from datetime import datetime
from core.extensions import base
from sqlalchemy.orm import column_property
from sqlalchemy import join , and_ ,select
from db_orm_models.data.gerencia import Gerencia
from db_orm_models.data.jefatura import  Jefatura
from db_orm_models.data.viceprecidencia import  Viceprecidencia
from db_orm_models.data.cargo import Cargo



class Colaborador  ( base, NamedCommonFields ):
    __tablename__ = "tm_colaborador"
    __table_args__ = {'comment': 'Tabla de datos de colaborador',}
    
    last_name = Column(String(128), nullable=False, unique=False)

    
    id_jefatura = Column(Integer , ForeignKey("ts_jefatura.id") , nullable=True ,comment = "Id de la jefatura del colaborador")
    id_viceprecidencia = Column(Integer , ForeignKey("ts_viceprecidencia.id") , nullable=True ,comment = "Id de la Viceprecidencia")
    id_gerencia = Column(Integer , ForeignKey("ts_gerencia.id") , nullable=True ,comment = "Id de la Gerencia")
    id_cargo = Column(Integer , ForeignKey("ts_cargo.id") , nullable=True)
    
    
Colaborador.gerencia = column_property(
    select(
        Gerencia.name

    ).where(
        Gerencia.id == Colaborador.id_gerencia
    ).correlate_except(Gerencia).limit(1)
)

Colaborador.jefatura = column_property(
    select(
        [Jefatura.name]
    ).where(
        Jefatura.id == Colaborador.id_jefatura
    ).correlate_except(Jefatura).limit(1)
)


Colaborador.viceprecidencia = column_property(
    select(
        [Viceprecidencia.name]
    ).where(
        Viceprecidencia.id == Colaborador.id_viceprecidencia
    ).correlate_except(Viceprecidencia).limit(1)
)


Colaborador.cargo = column_property(
    select(
        [Cargo.name]
    ).where(
        Cargo.id == Colaborador.id_cargo
    ).correlate_except(Cargo).limit(1)

)



