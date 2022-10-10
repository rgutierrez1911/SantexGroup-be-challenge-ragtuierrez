from app.api.v1.football.controller import router as football_router
from fastapi import FastAPI
from core.documentation.documentation import generar_ext_documentation


football_base_path = "/football"
football_app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title=f"{football_base_path.upper()} API V1.0",
    openapi_url="/swagger/openapi.json",
    swagger_ui_oauth2_redirect_url="/swagger/docs/oauth2-redirect")

prefix = "data"

football_app.include_router(football_router, prefix=f"/{prefix}")
generar_ext_documentation(app=football_app, base=football_base_path)
