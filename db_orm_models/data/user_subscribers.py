
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


class UserSubscribers (base, CommonFields):
  __tablename__ = "tm_user_subscribers"
  __table_args__ = {
      'comment': 'Table of user_subscribers',
  }

  user_id = Column(Integer, ForeignKey("tm_usuario.id"), nullable=False, index=True)
  subscriber_id = Column(Integer, ForeignKey("tm_usuario.id"), nullable=False, index=True)
  