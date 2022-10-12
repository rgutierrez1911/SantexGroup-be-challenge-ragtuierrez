from fastapi.openapi.docs import (
  get_redoc_html,
  get_swagger_ui_html,
  get_swagger_ui_oauth2_redirect_html,
)
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

STATIC_FILES_DIR = "commons/static" 

def generate_documentation(app:FastAPI , base_name:str = ""):
  print(f"--->{base_name}/swagger/docs")
  app.mount(f"{base_name}/swagger/static", StaticFiles(directory=STATIC_FILES_DIR), name="static")

  @app.get(f"{base_name}/swagger/docs", include_in_schema=False)
  async def custom_swagger_ui_html():
    print(f"{base_name}  {app.openapi_url}")
    return get_swagger_ui_html(
      openapi_url=f"{app.openapi_url}",
      title=f"API 1.0 {base_name}",
      oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
      swagger_js_url=f"{base_name}/swagger/static/swagger-ui-bundle.js",
      swagger_css_url=f"{base_name}/swagger/static/swagger-ui.css",
      swagger_favicon_url=f"{base_name}/swagger/static/favicon.ico",
    )


  @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
  async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


  @app.get("/swagger/redoc", include_in_schema=False)
  async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


def generar_ext_documentation(app: FastAPI , base:str = ""):

  app.mount("/swagger/static", StaticFiles(directory=STATIC_FILES_DIR), name="static")

  @app.get("/swagger/docs", include_in_schema=False)
  async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{base}{app.openapi_url}",
        title=f"{base} - API",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"{base}/swagger/static/swagger-ui-bundle.js",
        swagger_css_url=f"{base}/swagger/static/swagger-ui.css",
        swagger_favicon_url=f"{base}/swagger/static/favicon.ico",
    )


  @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
  async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


  @app.get("/swagger/redoc", include_in_schema=False)
  async def redoc_html():
    return get_redoc_html(
      openapi_url=f"{base}{app.openapi_url}",
      title=app.title + " - SOFTLAB",
      redoc_js_url=f"{base}/static/redoc.standalone.js",
    )
