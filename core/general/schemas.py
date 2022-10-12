from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import math
from dataclasses import dataclass
from fastapi import Query


class OrmModel(BaseModel):
  class Config:
    orm_mode = True


class Success(OrmModel):
  status:str = "Success"
  

class SuccessCreated(Success):
  id:int
  
class SuccessUpdated(Success):
  id:int


class DbUser(OrmModel):
  id:int 
  name:str
  mail:str
  state:str
  access_type:str
  active:bool
  full_name:str
  token:str = None



class UserAccess:

  def __init__(self,
               current_user: DbUser,
               session: Session,
               permitions: List[str] = None,
               token: str = None) -> None:
    
    self.permitions = permitions or []
    self.user = current_user
    self.db = session
    self.selected_permition = None
      
      
class CommonNamedBase(OrmModel):
  id:int
  register_date:datetime
  modified_date:datetime
  visible:bool
  active:bool
  name:str

class ClassNull(OrmModel):
  value: int = None

@dataclass
class Search:
  item_pagina: int = Query(10, gt=0)
  pag_actual: int = Query(1, gt=0)
  

class Pager(OrmModel):
  pag_anterior: int = None
  pag_actual: int = None
  pag_siguiente: int = None
  pag_total: int = None
  item_pagina: int = None
  item_desde: int = None
  item_hasta: int = None
  item_total: int = None
  data: List[ClassNull] = []
  pagination: str = None

  def count_item_total (self,db_sentence) ->int:
    return db_sentence.count()
  def get_data_offset (self , offset:int , db_sentence)->list:

    current_data = db_sentence.offset(
        offset
    ).limit(
        self.item_pagina
    ).all()
    return current_data

  def get_all_data(self , db_sentence) ->list:
    return db_sentence.all()
      
  def paginate(self, db_sentence=None):
    self.data = []
    self.pagination = self.pagination
    self.item_pagina = self.item_pagina
    offset = (self.pag_actual - 1) * self.item_pagina
    self.item_total = self.count_item_total(db_sentence=db_sentence)
    if self.item_total == 0:
      self.data = []
    else:
      self.data = self.get_data_offset(
          offset=offset, 
          db_sentence=db_sentence
      )


      # data_class:ClassNull=self.__annotations__["data"].__args__[0]

      self.pag_anterior = self.pag_actual - 1
      self.item_desde = 0 if self.item_total == 0 else (self.pag_anterior * self.item_pagina) + 1
      self.item_hasta = 0 if self.item_total == 0 else (self.pag_actual * self.item_pagina)
      self.pag_anterior = None if self.pag_anterior == 0 else self.pag_anterior

      self.pag_total = math.ceil(self.item_total / self.item_pagina)

      self.pag_siguiente = self.pag_actual + 1
      self.pag_siguiente = None if (
              self.pag_actual == self.pag_total or self.item_total == 0) else self.pag_siguiente
      self.item_hasta = self.item_total if self.item_hasta > self.item_total else self.item_hasta

      if self.pagination == 'false':
        self.pag_anterior = None
        self.pag_actual = None
        self.pag_siguiente = None
        self.pag_total = None
        self.item_pagina = None
        self.item_desde = None
        self.item_hasta = None
        self.item_total = None
        self.data = self.get_all_data(db_sentence=db_sentence)
        self.pagination = None