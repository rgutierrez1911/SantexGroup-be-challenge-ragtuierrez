
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
  Numeric,
  Text

)
from db_orm_models.data.common import CommonFields

from core.extensions import base


class Tweets (base, CommonFields):
  __tablename__ = "tm_tweets"
  __table_args__ = {
      'comment': 'Table of Tweets',
  }

  user_id = Column(Integer, ForeignKey("tm_usuario.id"), nullable=False, index=True)
  text = Column(String(256), nullable=False)
  
  