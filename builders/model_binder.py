from typing import Dict, List, Union, Tuple
from builders.schemas import DeleteSchema, SearchBase, Depends, SearchOnlyId
from commons.db_commons import create_base_model_data, create_base_model_get_data
from core.general.schemas import OrmModel, Success, SuccessCreated, SuccessUpdated
from db_orm_models.data.common import CommonFields, CustomField, NamedCommonFields, Session
from fastapi import APIRouter
from db_orm_models.data.school.grades import Grades
from dependencies.user_dependencies import UserAccess, user_db_permitions
from .exceptions import DbNotFoundException
from db_orm_models.data.common import to_dict

def get_data_from(
    base_query ,
    search_filter: Union[SearchBase, SearchOnlyId],
    model: CommonFields,
    args : Union[SearchBase, SearchOnlyId],

)->dict:
  
  if args.id:
    base_query = base_query.filter(model.id == args.id).all()

    return {"data": base_query}

  if issubclass(search_filter, SearchBase):
    
    if args.name:
      if isinstance(model, NamedCommonFields):
        base_query = base_query.filter(model.name.ilike(f"%{args.name}%")).all()
        return {"data": base_query}
    return {"data":  base_query.all()}
  
  return {"data": base_query.all()}

def get_list_orm_route_common(
    router: APIRouter,
    tags: List[str],
    model: CommonFields,
    permitions: List[str] = None,
    
    ):
  
  
  if permitions is None:
    permitions = []
  created_pydantic_model, name = create_base_model_get_data(model=model , addr_name="searched" , not_assignable= set() )
  
  pydantic_name = {"data": None}
  annotations = {"data": List[created_pydantic_model]}
  
  dinamic_values = {
      **pydantic_name,
      "__annotations__": annotations
  }
  
  if issubclass(model , NamedCommonFields):
    search_filter= SearchBase
  else:
    search_filter= SearchOnlyId
  
  
  new_out_type = type(name, (OrmModel,),  dinamic_values)
  custom_fields:List[Tuple[str , CustomField]] = []

  if getattr(created_pydantic_model, "__custom_fields", False) == True:
      for var_name in dir(model):
        current_field = getattr(model, var_name)
        if isinstance(current_field, CustomField):
          custom_fields.append((var_name, current_field))

  
  def search_base_model_function(
      args: search_filter = Depends(),
      user_access: UserAccess = user_db_permitions(permitions=permitions),
  )->List[created_pydantic_model]:

    base_query = user_access.db.query(
        model
    ).filter(
        model.active == True,
        model.visible == True,
    )

    model_data = get_data_from(base_query=base_query,
                               search_filter=search_filter,
                               model=model,
                               args=args)

    for custom_field in custom_fields:
      for row in model_data["data"]:
        field_name, field = custom_field
        
        field_data = field.get_data(model = Grades , db=user_access.db, value=row.id)
        setattr(row, field_name, field_data)

    return model_data

  new_get_route = router.get(f"/{name}",
                             tags=tags,
                             response_model=new_out_type,
                             name=name)


  new_get_route(search_base_model_function)
    

def create_orm_route_common(router: APIRouter,
                            tags: List[str],
                            model: CommonFields,
                            permitions: List[str] = None):
  if permitions is None:
    permitions = []

  created_pydantic_model, name = create_base_model_data(model=model)

  def created_model_function(
      args: created_pydantic_model,
      user_access: UserAccess = user_db_permitions(permitions=permitions),
  ):
    new_object = model(**args.dict())
    user_access.db.add(new_object)
    user_access.db.commit()
    return SuccessCreated(id=new_object.id)

  new_post_route = router.post(f"/{name}", tags=tags, response_model=SuccessCreated , name= name)

  new_post_route(created_model_function)

NOT_ASSIGNABLE = {
    "register_date",
    "modified_date",
    "visible",
    "active",
}
def update_orm_route_common(router: APIRouter,
                            tags: List[str],
                            model: CommonFields,
                            permitions: List[str] = None):

  if permitions is None:
    permitions = []

  created_pydantic_model, name = create_base_model_data(model=model,
                                                        addr_name="update",
                                                        not_assignable=NOT_ASSIGNABLE)
  
  def update_model_function(
      args: created_pydantic_model,
      user_access: UserAccess = user_db_permitions(permitions=permitions),
  ):

    updated_object = user_access.db.query(
        model
    ).filter(
        model.id == args.id,
        model.active == True
    ).first()
    
    if not updated_object:
      raise DbNotFoundException(status_code=404 , detail=f"ID {args.id} not found")
    
    dicted_args:dict = args.dict(exclude_unset=True)

    for key, val in dicted_args.items():
      setattr(updated_object, key, val)

    user_access.db.commit()
    return SuccessUpdated(id=updated_object.id)

  new_put_route = router.put(f"/{name}", tags=tags, response_model=SuccessUpdated, name=name)

  new_put_route(update_model_function)

def delete_orm_route_common(router: APIRouter,
                            tags: List[str],
                            model: CommonFields,
                            permitions: List[str] = None):

  if permitions is None:
    permitions = []

  
  def delete_model_function(
      id: int,
      user_access: UserAccess = user_db_permitions(permitions=permitions),
  ):

    updated_object = user_access.db.query(
        model
    ).filter(
        model.id == id,
        model.active == True
    ).first()
    
    updated_object.active = False
    user_access.db.commit()
    
    return Success()
  name = f"{model.__name__[0].lower()}{model.__name__[1:]}"
  
  new_delete_route = router.delete("/%s/{id}/delete"%(name), tags=tags, response_model=Success, name=f"{name}_delete")
  new_delete_route(delete_model_function)

def crud_routes_common(
    router: APIRouter,
    
    models: List[CommonFields],
    permitions: List[str] = None
):
  default_args = {
      
      "router": router,
      "permitions": permitions
  }
  to_execute = [get_list_orm_route_common,create_orm_route_common ,update_orm_route_common ,delete_orm_route_common]
  for model in models:  
    [func(**default_args ,tags= [model.__name__], model=model) for func in to_execute]
    


