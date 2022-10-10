


from operator import index
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
from db_orm_models.data.common import CommonFields

from core.extensions import base


class ProductsMetrics (base, CommonFields):
    __tablename__ = "tm_product_metrics"
    __table_args__ = {
        'comment': 'Table of products metrics',
    }

    id_product = Column(Integer, ForeignKey("tm_product.id"), nullable=False, index=True)
    id_user = Column(Integer, ForeignKey("tm_usuario.id"),nullable=True, index=True)
    times_queried = Column(Integer, nullable=False)
