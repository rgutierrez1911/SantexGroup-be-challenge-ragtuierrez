
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.documentation import documentation

from fastapi import staticfiles
from core.dbsetup import Base

from app.middlewares.startup import startup
from app.middlewares.every import add_process_time_header
#, add_jaeger_handler   
#*===================== MICRO SERVICES ======================
from commons.services.security import security_app , base_path
from app.services.football import football_app , football_base_path
#*===================== MICRO SERVICES ======================

#*===================== FULL FLEDGED SERVICES ======================
from app.api.v1.example.controller import router as example_router
from app.api.v1.users.controller import router as user_router
#*===================== FULL FLEDGED SERVICES ======================



app = FastAPI(
    docs_url=None, redoc_url=None,
    title="API V1.0",
    openapi_url="/swagger/openapi.json",
    swagger_ui_oauth2_redirect_url="/swagger/docs/oauth2-redirect",
    
    )
    

#? ADDING MIDDLWEARRES TO THE CURRENT APP
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(add_process_time_header)
# app.middleware("http")(add_jaeger_handler)
app.on_event("startup")(startup)



app.include_router(router=example_router, prefix="/api/v1/example-case")
app.include_router(router=user_router, prefix="/api/v1/users")




@app.get("/ping" , status_code=200)
def ping_service():
    return {"status": "success"}

#! MOUNTING THE SERVICES INDIVIDUALLY
app.mount(path=base_path, app=security_app, name= "security" )
app.mount(path=football_base_path , app=football_app , name="football")




print()
print ( "================ INITIALIZED MAIN SERVER ===================")
print()