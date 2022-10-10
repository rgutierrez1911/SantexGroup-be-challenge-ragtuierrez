

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


class Competition (base, NamedCommonFields):
    __tablename__ = "ft_competition"
    __table_args__ = {
        'comment': 'Table of Competition',
    }

    area_name = Column(String(96), nullable=False, unique=False)
    code = Column(String(96), nullable=False, unique=False)
    