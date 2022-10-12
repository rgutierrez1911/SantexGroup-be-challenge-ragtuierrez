
from sqlalchemy import VARCHAR, String, Integer, BigInteger, Float, Numeric, Boolean
from typing import List, Set, Tuple
from core.general.schemas import CommonNamedBase, OrmModel

from db_orm_models.data.common import CommonFields, CustomField, NamedCommonFields
from sqlalchemy.orm.attributes import InstrumentedAttribute

NOT_ASSIGNABLE = {
  "id",
  "register_date",
  "modified_date",
  "visible",
  "active",
}


def check_active(*models: List[CommonFields]) -> list:
  active_filter = [model.active == True for model in models]
  return active_filter


def check_visible(*models: List[CommonFields]) -> list:
  visible_filter = [model.visible == True for model in models]
  return visible_filter


def check_active_visible(*models: List[CommonFields]) -> List:
  model_filter_visible = check_active(*models)
  model_filter_active = check_visible(*models)

  return [*model_filter_active, *model_filter_visible]


def clone_model(model: CommonFields):

  # Ensure the model’s data is loaded before copying.
  model.id

  table = model.__table__
  non_pk_columns = [
      k for k in table.columns.keys() if k not in table.primary_key]
  data = {c: getattr(model, c) for c in non_pk_columns}
  data.pop('id')
  return data


def get_data_model(model: CommonFields):
  model.id

  table = model.__table__
  columns = [k for k in table.columns.keys()]
  data = [getattr(model, c) for c in columns]
  return data


def get_column_fields(
  model_fields: list,
  pydantic_name: dict,
  annotations: dict,
  fields_columns: list,

):
  for field_col in fields_columns:
    current_field = model_fields.columns[field_col]
    field_type = current_field.type
    if isinstance(field_type, String):
      annotations[current_field.name] = str
      pydantic_name[current_field.name] = ""

    elif isinstance(field_type, (Integer, BigInteger)):
      annotations[current_field.name] = int
      pydantic_name[current_field.name] = None

    elif isinstance(field_type, (Float, Numeric)):
      annotations[current_field.name] = float
      pydantic_name[current_field.name] = None
    elif isinstance(field_type, Boolean):
      annotations[current_field.name] = bool
      pydantic_name[current_field.name] = None
          

def get_custom_fields_columns(
    model: NamedCommonFields,
    pydantic_name: str,
    annotations: dict
):
  annotations["__custom_fields"] = bool
  
  
  for var_name in dir(model):
    current = getattr(model, var_name)
    if isinstance(current, CustomField):
      pydantic_name["__custom_fields"] = True
      annotations[var_name] = List[dict]
      pydantic_name[var_name] = []



def create_base_model_data(model: CommonFields, addr_name: str = "new", not_assignable: Set[str] = NOT_ASSIGNABLE) -> Tuple[OrmModel, str]:

  model_fields = model.__table__
  pydantic_model_name = f"{model.__name__}/{addr_name}"
  pydantic_route_name = f"{pydantic_model_name[0].lower()}{pydantic_model_name[1:]}"
  pydantic_model_name = f"{model.__name__}_{addr_name}"

  pydantic_name = {}
  annotations = {}

  fields_columns = set(model_fields.columns.keys()) - not_assignable
  get_column_fields(
    model_fields=model_fields,
    pydantic_name=pydantic_name,
    annotations=annotations,
    fields_columns=fields_columns,
  )

  dinamic_values = {
      **pydantic_name,
      "__annotations__": annotations
  }
  new_type = type(pydantic_model_name, (OrmModel,),  dinamic_values)
  return new_type, pydantic_route_name

def get_column_fields_additional(
  model: CommonFields,
  pydantic_name: dict,
  annotations: dict,

):
  column_names: Set[str] = set(model.__table__.columns.keys())

  instrumented_ref = {}
  for var_name in dir(model):
    current = getattr(model, var_name)
    if isinstance(current, InstrumentedAttribute):
      instrumented_ref[var_name] = current

  only_created: Set[str] = set(instrumented_ref.keys()) - column_names

  for created_field in only_created:
    annotations[created_field] = str
    pydantic_name[created_field] = None


def create_base_model_get_data(model: CommonFields,
                               addr_name: str = "searched",
                               not_assignable: Set[str] = NOT_ASSIGNABLE
                               ) -> Tuple[OrmModel, str]:
  model_fields = model.__table__
  pydantic_model_name = f"{model.__name__}/{addr_name}"
  pydantic_route_name = f"{pydantic_model_name[0].lower()}{pydantic_model_name[1:]}"
  pydantic_model_name = f"{model.__name__}_{addr_name}"

  pydantic_name, annotations = {}, {}

  fields_columns = set(model_fields.columns.keys()) - not_assignable
  
  if getattr(model , "additional_filters"):
    pass
  
  get_column_fields(
    model_fields=model_fields,
    pydantic_name=pydantic_name,
    annotations=annotations,
    fields_columns=fields_columns,
  )

  get_column_fields_additional(model=model,
                                pydantic_name=pydantic_name,
                                annotations=annotations)
  
  get_custom_fields_columns(model = model,
                            pydantic_name = pydantic_name,
                            annotations = annotations)

  dinamic_values = {
    **pydantic_name,
    "__annotations__": annotations
  }

  new_type = type(pydantic_model_name, (OrmModel,),  dinamic_values)

  return new_type, pydantic_route_name
