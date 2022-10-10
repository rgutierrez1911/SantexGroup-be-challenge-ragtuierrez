### LLAVE SECRETA
from dotenv import load_dotenv 
from pathlib import Path
import os
env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path, override=True)
envsettings = os.getenv("ENV" , "dev")

SECRET_KEY =os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int ( os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")  ) 
REFRESH_TOKEN_EXPIRE_MINUTES =  int ( os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")  ) 

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST" , "localhost")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
INCLUDE_SCHEMA = os.getenv("INCLUDE_SCHEMA")

BIBLIOTECA = os.getenv("BIBLIOTECA" , "/Biblioteca/")
RUTA_BIBLIOTECA=   os.getenv("RUTA_BIBLIOTECA")
 
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = os.getenv("LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN")
LDAP_AUTH_URL = os.getenv("LDAP_AUTH_URL")
LDAP_AUTH_CONNECT_TIMEOUT = os.getenv("LDAP_AUTH_CONNECT_TIMEOUT")
LDAP_AUTH_AUTHENTICATION = os.getenv("LDAP_AUTH_AUTHENTICATION")
LDAP_AUTH_RECEIVE_TIMEOUT = os.getenv("LDAP_AUTH_RECEIVE_TIMEOUT")
LDAP_AUTH_USE_TLS = os.getenv("LDAP_AUTH_USE_TLS")
LDAP_AUTH_SEARCH_BASE = os.getenv("LDAP_AUTH_SEARCH_BASE")

MAIL_SERVER = os.getenv("MAIL_SERVER" , "127.0.0.1")

MAIL_PORT = os.getenv("MAIL_PORT" , 1025)
MAIL_USER = os.getenv("MAIL_USER" , "admin@test.com")
MAIL_PWD= os.getenv("MAIL_PWD" , "admin")

IS_SERVER_DUMMY:int = os.getenv("IS_SERVER_DUMMY" ,1)
## CELERY CONFIGURATION ###
CELERY_DB_TYPE = os.getenv("CELERY_DB_TYPE")
CELERY_USERNAME = os.getenv("CELERY_USERNAME")
CELERY_PASSWORD = os.getenv("CELERY_PASSWORD")
CELERY_HOST = os.getenv("CELERY_HOST")
CELERY_PORT = os.getenv("CELERY_PORT")

CELERY_QUEUE = os.getenv("CELERY_QUEUE")
CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE")

CELERY_REDIS_POINT = os.getenv("CELERY_REDIS_POINT", None)

WAIT=os.getenv("WAIT" , "TRUE")

API_KEY = os.getenv("API-KEY" , "01e5cb27e62c4fb1a39778227392ba79")