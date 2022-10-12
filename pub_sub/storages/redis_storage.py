
from contextlib import contextmanager
from email import message
from time import sleep
import redis
from typing import List

from .base_storage import BaseStorage



class RedisStorage(BaseStorage):
  #*This class is created to serve in a lambda thats why it's not using a Ctx manager
  def connect(self):
    self.connection = redis.Redis(
        host=self.host,
        port=self.port,
        db=int(self.db),
        decode_responses=True
    )
    print(self)

    return self.connection

  def close(self):
    self.connection.close()
      
  def __enter__(self):
    self.connect()
    return self
  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.close()
