

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


class Product (base, NamedCommonFields):
    __tablename__ = "tm_product"
    __table_args__ = {
        'comment': 'Table of products',
    }

    name = Column(String(96), nullable=False, unique=False, index=True)
    price = Column(Numeric(precision=12,scale=2, asdecimal=False))

    