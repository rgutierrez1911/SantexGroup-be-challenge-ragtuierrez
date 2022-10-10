from pydantic import BaseModel
from fastapi import Query , Depends
from dataclasses import dataclass
class DeleteSchema(BaseModel):
  id:int
  
@dataclass
class SearchBase:
  name : str = Query(None)
  id :int = Query(None)

  
@dataclass
class SearchOnlyId:
  id :int = Query(None)
  