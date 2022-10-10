# write you database models in this file
from dataclasses import dataclass
from typing import Any, Dict, List, Optional , Union
from db_orm_models.data import (Column,
                      BigInteger,
                      String,
                      Boolean,
                      TIMESTAMP,
                      Identity)

from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.orm import Session , InstrumentedAttribute

class CommonFields:
  id = Column(BigInteger,Identity(start=1, cycle=True), primary_key=True , autoincrement = True)
  register_date = Column(TIMESTAMP, nullable=False, default=datetime.now)
  modified_date = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
  visible = Column(Boolean, server_default="true", nullable=False)
  active = Column(Boolean, server_default="true", nullable=False)
  
  
  @property
  def is_available_filters(self,)->List:
    return [self.active == True, self.visible == True]

    
class BaseNamedCommonFields(CommonFields):
  name = Column(String(96), nullable=False, unique=False)

class NamedCommonFields(BaseNamedCommonFields):
  name = Column(String(96), nullable=False, unique=False)
  
  @classmethod
  def find_by_id_name(cls,
                      db: Session,
                      current_id: Optional[int] = None,
                      current_name: Optional[str] = None,
                      first: bool = False
                      ) -> Union[List[BaseNamedCommonFields], BaseNamedCommonFields]:
    from commons.db_commons import check_active_visible
    common_local_filter = check_active_visible(cls)
    current_query = db.query(cls).filter(*common_local_filter)

    if current_id:
        current_query = current_query.filter(cls.id == current_id)
    elif current_name:
        current_query = current_query.filter(
            cls.name.ilike(f"%{current_name}%"))
    if first:
        only_one: BaseNamedCommonFields = current_query.first()
        return only_one
    multiple: List[NamedCommonFields] = current_query.all()
    return multiple
  
  @classmethod
  def find_by_ids(cls, db: Session, current_ids: List[int]) -> list:
    from commons.db_commons import check_active_visible
    common_local_filter = check_active_visible(cls)

    return db.query(cls).filter(
        *common_local_filter,
        cls.id.in_(current_ids)
    ).all()


def to_dict(model: CommonFields, queried: list) -> list:
  inspected = inspect(model).mapper.column_attrs
  
  rows = [{ele.key: getattr(row, ele.key)
           for ele in inspected} for row in queried]
  return rows


@dataclass
class CustomField:
  field_name: str = "name"
  
  def _get_minimal_columns(self , model : CommonFields , excluded:List[str] = None):  
    if not excluded:
      excluded = [
        "register_date",
        "modified_date",
        "visible",
        "active",
      ]
    
    current_fields: Dict[str, InstrumentedAttribute] = {}
    to_return_fields: List[Union[InstrumentedAttribute, CustomField]] = []

    for field in dir(model):
      field_ref = getattr(model, field)
      
      if isinstance(field_ref, (InstrumentedAttribute, CustomField)):
        current_fields[field] = field_ref

    for field_key, field_val in current_fields.items():
      if field_key not in excluded:
        to_return_fields.append(field_val)
      
    return to_return_fields

  def get_data(
      self,
      model: CommonFields,
      db: Session,
      value: Any,
      validate_active: bool = False,
      exclude_internal: bool = True,
      params: List[dict] = []
  ):

    query = db.query(
        model
    ).filter(
        getattr(model, self.field_name) == value
    )

    query = query.filter(*model.is_available_filters) if validate_active else query
    
    if params:
      for param in params:
        keys, values = param.items()
        for key, pvalue in zip(keys, values):
          query = query.filter(getattr(model, key) == pvalue)

    if exclude_internal:
      query = query.with_entities(
          *self._get_minimal_columns(model=model)
      )
      
    queried = query.all()

    if len(queried) > 0:
      if not exclude_internal:
        dicted_rows = to_dict(model=model, queried=queried)
        return dicted_rows
      return [row._asdict() for row in queried]
    return []
