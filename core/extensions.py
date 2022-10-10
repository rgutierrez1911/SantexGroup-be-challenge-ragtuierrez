from typing import Callable
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine
from core.factories import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, ForeignKey, Integer, String, Boolean ,Float , ForeignKey ,BigInteger,  TIMESTAMP
from sqlalchemy.orm import scoped_session
from contextlib import contextmanager
from core.factories import settings
from starlette.requests import Request
from sqlalchemy.orm import Session
from functools import wraps

engine = create_engine(settings.DATABASE_URL , max_identifier_length = 128)

metadata = MetaData()


base = declarative_base(bind = engine , metadata=metadata )

current_session = sessionmaker(bind=engine)
session = scoped_session(current_session)


def yield_session()->Session:
    try :
        yield session
    finally:
        print("CLOSING DB SESSION")
        session.close()

def get_session():
    return session


def session_decorator(func: Callable):
    @wraps(func)
    def wrapper(*args,  **kwargs):
        try:
            kwargs["db"] = session
            return func(*args, **kwargs)
        finally:
            session.close()
    return wrapper
