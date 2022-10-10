from starlette.config import Config
from starlette.datastructures import Secret, URL
from core.settings.settings import BaseConfig
import core.config as core_config

class ProdSettings(BaseConfig):

    """ Configuration class for site development environment """

    config = Config()
    DEBUG = config("PROD", cast=bool, default=True)
    ALGORITHM = core_config.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = core_config.ACCESS_TOKEN_EXPIRE_MINUTES
    DB_USER = core_config.DB_USER
    DB_PASSWORD = core_config.DB_PASSWORD
    DB_HOST = core_config.DB_HOST
    DB_PORT = core_config.DB_PORT
    DB_NAME = core_config.DB_NAME
    INCLUDE_SCHEMA = core_config.INCLUDE_SCHEMA

    CELERY_DB_TYPE = core_config.CELERY_DB_TYPE
    CELERY_USERNAME = core_config.CELERY_USERNAME
    CELERY_PASSWORD = core_config.CELERY_PASSWORD
    CELERY_HOST = core_config.CELERY_HOST
    CELERY_PORT = core_config.CELERY_PORT
    CELERY_QUEUE = core_config.CELERY_QUEUE
    CELERY_TIMEZONE = core_config.CELERY_TIMEZONE
    CELERY_REDIS_POINT = core_config.CELERY_REDIS_POINT
    
    REFRESH_TOKEN_EXPIRE_MINUTES = core_config.REFRESH_TOKEN_EXPIRE_MINUTES

    DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    DATABASE_URL = config("DATABASE_URL", default=DB_URL)

    CELERY_URL = f"{CELERY_DB_TYPE}://{CELERY_HOST}:{CELERY_PORT}/{CELERY_REDIS_POINT}"

