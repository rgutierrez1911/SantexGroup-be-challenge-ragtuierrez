from starlette.config import Config
from starlette.datastructures import Secret
import os

project_name="fast_api_service"


class BaseConfig:

    """
    Base configuration class. Subclasses should include configurations for
    testing, development and production environments
    """
    config = Config()

    INCLUDE_SCHEMA=config("INCLUDE_SCHEMA", cast=bool, default=True)

    SECRET_KEY = config("SECRET_KEY",default=os.urandom(32))
    
    SQLALCHEMY_ECHO = config("SQLALCHEMY_ECHO",cast=bool,default=False)
    SQLALCHEMY_TRACK_MODIFICATIONS = config("SQLALCHEMY_TRACK_MODIFICATIONS",cast=bool,default=False)

    LOGGER_NAME = "%s_log" % project_name
    LOG_FILENAME = "/var/tmp/app.%s.log" % project_name

    CORS_ORIGINS = config("CORS_HOSTS",default="*")



    DEBUG = config("DEBUG", cast=bool, default=False)
    TESTING = config("TESTING", cast=bool, default=False)

    API_KEY = os.getenv("API-KEY" , "01e5cb27e62c4fb1a39778227392ba79")