
from fastapi import FastAPI

from core.documentation.documentation import generar_ext_documentation
from core.constants import modify_token_path

base_path = "/security"
security_app = FastAPI(
  docs_url=None,
  redoc_url=None,
  title=f"{base_path.upper()} API V1.0",
  openapi_url="/swagger/openapi.json",
  swagger_ui_oauth2_redirect_url="/swagger/docs/oauth2-redirect")

security_prefix = "auth"
token_path = modify_token_path(
  base_path=base_path,
  controller=security_prefix,
  actual_path="token")

print(f"new_token path >>>> {token_path}")
from commons.controllers.security.controller import router as auth_router
security_app.include_router(auth_router, prefix=f"/{security_prefix}")
generar_ext_documentation(app=security_app, base=base_path)


# def generate_security_app(
#     base_path: str = "/security",
#     security_prefix: str = "auth"
# ):
#     security_app = FastAPI(
#         docs_url=None,
#         redoc_url=None,
#         title=f"{base_path.upper()} API V1.0",
#         openapi_url="/swagger/openapi.json",
#         swagger_ui_oauth2_redirect_url="/swagger/docs/oauth2-redirect")

#     token_path = modify_token_path(
#         base_path=base_path,
#         controller=security_prefix,
#         actual_path="token")

#     print(f"new_token path >>>> {token_path}")
#     from commons.controllers.security.controller import router as auth_router
#     security_app.include_router(auth_router, prefix=f"/{security_prefix}")
#     generar_ext_documentation(app=security_app, base=base_path)

#     return security_app , base_path
