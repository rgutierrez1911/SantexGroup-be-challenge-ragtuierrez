

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
    Sequence,
    Numeric

)
from db_orm_models.data.common import CommonFields, NamedCommonFields

from core.extensions import base


class Players (base, NamedCommonFields):
    __tablename__ = "ft_players"
    __table_args__ = {
        'comment': 'Table of Players',
    }

    position = Column(String(96), nullable=True, unique=False)
    date_of_birth = Column(String(96), nullable=True, unique=False)
    nationality = Column(String(96), nullable=True, unique=False)
    
    id_team =   Column(Integer , ForeignKey("ft_teams.id"))
    


class Coachs (base, CommonFields):
    __tablename__ = "ft_coach"
    __table_args__ = {
        'comment': 'Table of Coach',
    }
    
    name = Column(String(96), nullable=True, unique=False)
    date_of_birth = Column(String(96), nullable=True, unique=False)
    nationality = Column(String(96), nullable=True, unique=False)
    
    id_team =   Column(Integer , ForeignKey("ft_teams.id") , index = True)