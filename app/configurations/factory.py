from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.') / '.env'

load_dotenv(env_path)

SECRET_KEY = os.getenv("SECRET_KEY", None)
ALGORITHM = os.getenv("ALGORITHM", None)
ACCESS_TOKEN_EXPIRE_MINUTES = int ( os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 240))
REFRESH_TOKEN_EXPIRE_MINUTES= int ( os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 560))