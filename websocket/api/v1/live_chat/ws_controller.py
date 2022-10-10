from fastapi import WebSocket
from core.security import DbUser
from datetime import datetime as dt
from .managers import WsRoomManager , WsConnectionManager

ws_room = WsRoomManager(room_name = "UserChat")


async def manage_ws_controller(
    ws: WebSocket,
    db_user: DbUser,
):
    global ws_room
    
    # await ws.accept()
    new_connection=WsConnectionManager(ws = ws , db_user=db_user)
    await ws_room.add_ws_user(
        ws_conn=new_connection
    )
    
    
    await new_connection.listen()


def get_ws_room_current ()->WsRoomManager:
    global ws_room
    
    return ws_room