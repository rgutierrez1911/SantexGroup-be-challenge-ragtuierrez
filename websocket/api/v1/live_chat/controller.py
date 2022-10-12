from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from core.general.schemas import Success
from .services import get_ws_users_group_names, render_websocket_page ,send_message_ws_api

from datetime import datetime as dt
from dependencies.user_dependencies import user_db_permitions , UserAccess
from core.security import get_current_user_ws,DbUser
from .ws_controller import manage_ws_controller
from .schemas import SendMessageApi, WsListUsers , SearchProduct

tags = ["LIVE-CHAT"]

router = APIRouter()

@router.get("/auth" ,tags=tags , response_model=Success)
async def get(
  user_access: UserAccess = user_db_permitions(),
):
  return Success()

@router.get("" , tags=tags)
async def get(
  # user_access: UserAccess = user_db_permitions(),
):
  rendered_html = render_websocket_page(auth_token="test")
  return HTMLResponse(rendered_html)


@router.websocket("/ws")
async def chat_service(
  ws_params=Depends(get_current_user_ws)

):
  user, websocket = ws_params
  await manage_ws_controller(
    ws=websocket,
    db_user=user
  )


@router.get("/list-chat-users", tags=tags, response_model=WsListUsers)
async def list_ws_connections(
  user_access: UserAccess = user_db_permitions(),
  args: SearchProduct = Depends(SearchProduct)
):
  current_user_ws_name = f"{user_access.user.id}-{user_access.user.name}"

  ws_users = get_ws_users_group_names()
  if args.filter_current:
    data = [ws_user for ws_user in ws_users if ws_user != current_user_ws_name]
  else:
    data = ws_users

  return {
    "data": data
  }


@router.post("/send-message/ws", tags=tags, response_model=Success)
async def send_mesage_ws_api(
  args : SendMessageApi ,
  user_access: UserAccess = user_db_permitions(),
):
  await send_message_ws_api(names= args.ws_names , message=args.message)
  return Success()
