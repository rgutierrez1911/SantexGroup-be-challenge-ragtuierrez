from typing import List
from core.renderers.html_util import render_html
from .ws_controller import get_ws_room_current

from .schemas import ConnectionManagerBaseSchema, ConnectionRoomManagerBaseSchema
WEBSOCKET_TEMPLATE = "live-chat.html"
TEMPLATE_FOLDER = "websocket/templates/"


def render_websocket_page(
    auth_token: str
) -> str:

    rendered_html = render_html(template_file=WEBSOCKET_TEMPLATE,
                                args={"auth_token": auth_token},
                                template_folder=TEMPLATE_FOLDER)
    return rendered_html


def get_ws_users_group_names():
    ws_room = get_ws_room_current()
    ws_groups = list(ws_room.ws_users.keys())

    return ws_groups


def get_ws_user_groups_managers(names: List[str] = None):
    ws_room = get_ws_room_current()
    if names:
        ws_managers = ws_room.get_by_identifier(identifiers_name=names)
    else:
        ws_managers = ws_room.get_all_ws_managers()

    return ws_managers


async def send_message_ws_api(
    names: List[str],
    message: str,

):

    payload = {"message": message}
    ws_room = get_ws_room_current()
    connection_proxy = ConnectionManagerBaseSchema()

    await ws_room.send_message_groups(names=names,
                                      payload=payload,
                                      connection_proxy=connection_proxy)
