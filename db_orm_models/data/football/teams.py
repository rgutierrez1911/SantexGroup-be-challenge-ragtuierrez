

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


class Teams (base, NamedCommonFields):
    __tablename__ = "ft_teams"
    __table_args__ = {
        'comment': 'Table of Teams',
    }

    area_name = Column(String(96), nullable=True, unique=False)
    tla = Column(String(96), nullable=True, unique=False)
    short_name = Column(String(96), nullable=True, unique=False)
    address =Column(String(256), nullable=True, unique=False)

class TeamsCompetition (base, CommonFields):
    __tablename__ = "ft_teams_competition"
    __table_args__ = {
        'comment': 'Table of TeamsCompetition',
    }

    id_competition = Column(Integer , ForeignKey("ft_competition.id") , index= True)
    id_team = Column(Integer , ForeignKey("ft_teams.id") , index= True)
