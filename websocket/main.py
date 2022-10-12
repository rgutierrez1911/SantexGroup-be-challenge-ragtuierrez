from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.documentation import documentation
from core.dbsetup import Base


#! COMMON SERVICES
from commons.services.security import security_app , base_path
#! COMMON SERVICES

#!ROUTER
from .api.v1.live_chat.controller import router as live_chat_router


app = FastAPI(
    docs_url=None, redoc_url=None,
    title="WEBSOCKET - API V1.0",
    openapi_url="/swagger/openapi.json",
    swagger_ui_oauth2_redirect_url="/swagger/docs/oauth2-redirect",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", status_code=200)
def ping_service():
  return {"status": "success"}


app.mount(path=base_path, app=security_app, name="security")

app.include_router(router=live_chat_router, prefix="/api/v1/live-chat")


documentation.generate_documentation(app=app, base_name="/ws")

print()
print ( "================ INITIALIZED WEBSOCKET SERVER ===================")
print()