

from typing import Coroutine, Dict, List
from fastapi import WebSocket
from core.security import DbUser
import asyncio
from datetime import datetime as dt
from starlette.websockets import WebSocketState, WebSocketDisconnect
from copy import deepcopy
from .schemas import ConnectionManagerBaseSchema

from enum import Enum
from dataclasses import dataclass, field


class CommandsEnum(Enum):
    CONNECTED = 1
    WS_NEW_CONNECTION = 99


@dataclass
class WsConnectionManagerBase:

    ws: WebSocket
    db_user: DbUser
    connection_name: str = field(default="")
    group_name: str = field(default="")
    room: "WsRoomManagerBase" = field(default=None)
    ready: bool = field(default=None)
    client_state: WebSocketState = field(default=None)
    group_manager: "WsGroupConnectionManagerBase" = field(default=None)

    async def accept_connection(self): pass
    async def auto_send(self, data: dict): pass

    async def send_multiple_by_group(self,
                                     group_managers: List["WsGroupConnectionManagerBase"],
                                     data: dict
                                     ): pass

    async def on_listen_execute(self, data: dict): pass
    async def listen(self): pass


@dataclass
class WsGroupConnectionManagerBase:
    room: "WsRoomManagerBase"
    group_name: str = field( default="")
    connections: List[WsConnectionManagerBase] = field(default_factory=list)

    def add(self, connection: WsConnectionManagerBase):pass
    async def on_disconnect_remove(self, connection: WsConnectionManagerBase):pass
    
    async def send_message_group(self,
                                 payload: dict): ...

@dataclass
class WsRoomManagerBase:

    room_name: str = field(default="General")
    ws_users: Dict[str, WsGroupConnectionManagerBase]  =field(default_factory= dict)
    log_room_messages: List[str] = field(default_factory=list)
    
    

    async def add_ws_user(self, ws_conn: WsConnectionManagerBase):pass
    
    def get_by_identifier(self,
                          identifiers_name: List[str] = None,
                          ) -> List[WsGroupConnectionManagerBase]:pass
    
    async def send_message_groups(self,
                                  names: List[str],
                                  payload: dict,
                                  connection_proxy: ConnectionManagerBaseSchema):pass
    
    async def send_new_connection_broadcast(self, group_name: str, ):pass
    def get_all_ws_managers(self) -> List[WsGroupConnectionManagerBase]:pass
    def add_log_room_messages(self, message: dict):pass

def add_ws_info(payload: dict, connection: WsConnectionManagerBase):
    payload["origin_ws_info"] = {
        "name": connection.connection_name,
        "room_name": connection.room.room_name,
        "current_timestamp": dt.now().isoformat(),
        "group_name": connection.group_name,
    }


def generate_payload(
    connection: WsConnectionManagerBase,
    payload: dict = {},
):

    new_payload = deepcopy(payload)
    add_ws_info(payload=new_payload, connection=connection)

    return new_payload


def generate_command_payload(connection: WsConnectionManagerBase,
                             message: str,
                             command: str,
                             ws_users: List[str],
                             ):

    payload = {
        "message": message,
        "command": command,
        "connected_ws_users": ws_users

    }
    add_ws_info(payload=payload, connection=connection)

    return payload

@dataclass
class WsConnectionManager(WsConnectionManagerBase):
    def __init__(self, ws: WebSocket, db_user: DbUser) -> None:
        self.ws = ws
        self.db_user = db_user
        self.ready = False
        self.connection_name: str = None
        self.group_name: str = None
        self.room: WsRoomManager = None
        self.client_state = None
        self.group_manager: WsGroupConnectionManagerBase = None

    async def accept_connection(self):
        await self.ws.accept()
        self.ready = True
        self.client_state = self.ws.client_state

        group_names = [
            manager.group_name for manager in self.room.get_all_ws_managers()]

        payload = generate_command_payload(
            connection=self,
            message=self.connection_name,
            command=self.client_state.name,
            ws_users=group_names
        )

        await self.auto_send(data=payload)
        await self.room.send_new_connection_broadcast(group_name=self.group_name)

    async def auto_send(self, data: dict):
        print(f"STATE WS -> {self.client_state}")
        if self.client_state.value == WebSocketState.CONNECTED.value:
            await self.ws.send_json(data=data)
        else:
            print(
                f"Not connected {self.connection_name} -> {self.client_state.name} - {self.client_state.value}")
            print(self.room.ws_users)

    async def send_multiple_by_group(self,
                                     group_managers: List[WsGroupConnectionManagerBase],
                                     data: dict
                                     ):
        for ws_manager_group in group_managers:
            to_send = []
            for ws_manager in ws_manager_group.connections:

                print(f"Sending on WS -> {ws_manager.connection_name}")
                to_send.append(ws_manager.auto_send(data=data))
            await asyncio.gather(*to_send)

    async def on_listen_execute(self, data: dict):

        command = data.get("command", "ECHO")
        payload: dict = data.get("payload", {})
        targets: List[str] = data.get("targets", [])

        sender_payload = generate_payload(payload=payload, connection=self)
        print(f"payload WS -> {payload}")

        if command == "ECHO":
            await self.auto_send(data=sender_payload)

        elif command in ["GROUPCAST", "MONOCAST"]:
            retrieved_ws_managers = self.room.get_by_identifier(
                identifiers_name=targets)

            await self.send_multiple_by_group(
                group_managers=retrieved_ws_managers,
                data=sender_payload
            )
        elif command == "BROADCAST":
            retrieved_ws_managers = self.room.get_all_ws_managers()

            await self.send_multiple_by_group(
                group_managers=retrieved_ws_managers,
                data=sender_payload
            )
        else:
            await self.auto_send(data=sender_payload)

        self.room.add_log_room_messages(message=sender_payload)

    async def listen(self):

        while True:
            try:
                data = await self.ws.receive_json()

                await self.on_listen_execute(data=data)

            except WebSocketDisconnect as ws_disconnect:

                self.client_state = WebSocketState.DISCONNECTED
                await self.group_manager.on_disconnect_remove(connection=self)

                return

            except Exception as ex:

                return

@dataclass
class WsGroupConnectionManager(WsGroupConnectionManagerBase):

    def add(self, connection: WsConnectionManager):
        connection.group_manager = self
        self.connections.append(connection)

    async def send_message_group(self,
                                 payload: dict):
        to_auto_send_msgs = []

        for connection in self.connections:
            auto_send_msgs = connection.auto_send(data=payload)
            to_auto_send_msgs.append(auto_send_msgs)

        await asyncio.gather(*to_auto_send_msgs)

    def on_disconnect_remove(self, connection: WsConnectionManagerBase):
        try:

            for idx, conn in enumerate(self.connections):
                if conn.connection_name == connection.connection_name:
                    self.connections.pop(idx)


                
            if len(self.connections) == 0:
                group_name = f"{self.group_name}"
                self.room.ws_users.pop(group_name, None)
                self.room.send_new_connection_broadcast(group_name=group_name)
                
                
                

        except ValueError as ex:
            print("Couldn't remove from Group Manager Because it Doesn't exist")
            

    def __repr__(self) -> str:
        connections = ""
        for conn in self.connections:
            connections = f"{connections} <{conn.connection_name} - {conn.client_state.name}> "
        return connections

@dataclass
class WsRoomManager(WsRoomManagerBase):


    async def add_ws_user(self, ws_conn: WsConnectionManager):
        connection_name = f"{ws_conn.db_user.id}-{ws_conn.db_user.name}"
        group_manager: WsGroupConnectionManagerBase = self.ws_users.get(
            connection_name)

        if not group_manager:
            group_manager = WsGroupConnectionManager(group_name=connection_name,
                                                     room=self)

            self.ws_users[connection_name] = group_manager

        num_connection = len(group_manager.connections)

        ws_conn.connection_name = f"{connection_name}-[{num_connection}]"
        ws_conn.group_name = connection_name
        ws_conn.room = self

        group_manager.add(connection=ws_conn)

        await ws_conn.accept_connection()

    def get_by_identifier(self,
                          identifiers_name: List[str] = None,
                          ) -> List[WsGroupConnectionManager]:
        extracted_ws_managers = []
        if identifiers_name is None:
            identifiers_name = []

        for identifier in identifiers_name:
            current_ws_retrieved = self.ws_users.get(identifier)
            extracted_ws_managers.append(current_ws_retrieved)

        return extracted_ws_managers

    async def send_message_groups(self,
                                  names: List[str],
                                  payload: dict,
                                  connection_proxy: ConnectionManagerBaseSchema):

        to_send = []
        group_managers = self.get_by_identifier(identifiers_name=names)

        generated_payload = generate_payload(payload=payload,
                                             connection=connection_proxy)
        for group_manager in group_managers:
            sender_msg = group_manager.send_message_group(
                payload=generated_payload)
            to_send.append(sender_msg)

        await asyncio.gather(*to_send)

    async def send_new_connection_broadcast(self, group_name: str, ):

        to_send: List[Coroutine] = []

        server_proxy_connection = ConnectionManagerBaseSchema()

        generated_payload = generate_command_payload(
            connection=server_proxy_connection,
            message=group_name,
            command=CommandsEnum.WS_NEW_CONNECTION.name,
            ws_users=[*self.ws_users.keys()]
        )

        for ws_user_group in self.get_all_ws_managers():

            msg_to_send = ws_user_group.send_message_group(
                payload=generated_payload)
            to_send.append(msg_to_send)

        await asyncio.gather(*to_send)

    def get_all_ws_managers(self) -> List[WsGroupConnectionManager]:
        return list(self.ws_users.values())

    def add_log_room_messages(self, message: dict):
        self.log_room_messages.append(message)
