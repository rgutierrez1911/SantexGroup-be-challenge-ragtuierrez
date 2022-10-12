from typing import Optional
from datetime import datetime, timedelta
from commons.configurations import (SECRET_KEY,
                                  ALGORITHM,
                                  ACCESS_TOKEN_EXPIRE_MINUTES,
                                  REFRESH_TOKEN_EXPIRE_MINUTES)

from core.exceptions.auth import invalid_jwt_token
from core.security import validate_expired
from jose import jwt
from core.factories import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire, "type": "access"})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire, "type": "refresh"})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def decode_jwt(token:str ,enforced_token_type:str):
  payload: dict = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
  username: str = payload.get("sub")
  token_type: str = payload.get("type", None)
  id_user:str = payload.get("id_user",  None)
  exp = payload.get("exp")
  validate_expired(exp=exp, leeway=0)

  if token_type != enforced_token_type:
    raise invalid_jwt_token
  return username , id_user


def decode_refresh_jwt(token: str, enforced_token_type: str):
  payload: dict = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

  username: str = payload.get("sub")
  token_type: str = payload.get("type", None)
  id_user: str = payload.get("id_user",  None)
  exp = payload.get("exp")
  validate_expired(exp=exp, leeway=0, detail="REFRESH-TOKEN-EXPIRED")
  
  if token_type != enforced_token_type:
    raise invalid_jwt_token
  return username , id_user
