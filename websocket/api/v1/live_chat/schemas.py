from typing import List
from core.general.schemas import OrmModel
from fastapi import Query
from dataclasses import dataclass


class WsListUsers(OrmModel):
  data: List[str] = []


@dataclass
class SearchProduct:

    filter_current: bool = Query(True)


class SendMessageApi(OrmModel):
  ws_names: List[str] 
  message: str

class ConnectionRoomManagerBaseSchema(OrmModel):
  room_name :str ="Ws_server"
  
class ConnectionManagerBaseSchema(OrmModel):
  connection_name : str = "Ws_server"
  room:ConnectionRoomManagerBaseSchema = ConnectionRoomManagerBaseSchema()
  group_name:str = "Ws_server"