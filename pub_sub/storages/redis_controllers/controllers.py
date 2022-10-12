# from pub_sub.storages.redis_storage import RedisStorage
from ..redis_storage import RedisStorage
import json
import redis
from typing import Generator, List, Union
from time import sleep
from logging import basicConfig , getLogger

FORMAT = "%(asctime)-5s : %(levelname)-8s %(message)s"

basicConfig(format=FORMAT)
logger = getLogger()


class RedisSimpleKey:
  def __init__(self, storage: RedisStorage, name: str) -> None:
    if not storage.connection:
      storage.connect()

    self.name = name
    self.storage_connection: redis.Redis = storage.connection

  def set(self, data: str):
    self.storage_connection.set(self.name, data)

  def get(self):
    data: str = self.storage_connection.get(self.name)
    return data

    
class RedisPublisher:
  def __init__(self, storage: RedisStorage, name: str) -> None:
    if not storage.connection:
      storage.connect()

    self.name = name
    self.storage_connection: redis.Redis = storage.connection

  def publish_message(self, data: dict):
    stringed_data = json.dumps(data)
    print(f"{self.name} -> {stringed_data}")
    self.storage_connection.publish(
      channel=self.name, message=stringed_data)


class RedisSubscriber:
  def __init__(self, storage: RedisStorage, name: str) -> None:
    if not storage.connection:
      storage.connect()
    self.name = name
    self.storage_connection: redis.Redis = storage.connection
    self.subcriber = self.storage_connection.pubsub()
    self.subcriber.subscribe(self.name)

  def listen(self) -> Generator[dict, None, None]:
    for message in self.subcriber.listen():
      if message:
        if "data" in message:
          try:
            data:dict = json.loads(message["data"])
            yield data
          except:
            print("No current data ATM")

class RedisQueue:
  def __init__(self, storage: RedisStorage, name: str) -> None:
    if not storage.connection:
      storage.connect()
        
    self.storage = storage
    self.name = name
    self.storage_connection:redis.Redis = storage.connection
    logger.info(f"connected to redis DB {self.storage_connection}")
    print(f"connected to redis DB {self.storage_connection}")

  def enque(self, data: dict)->None:
    json_data = json.dumps(data)
    logger.info(f"enquing {self.name} -> sending {json_data}")
    print (f"enquing {self.name} -> sending {json_data}")
    self.storage_connection.lpush(self.name, json_data)
    
  def enque_multiple (self, messages : List[dict]):
    json_data = [json.dumps(message) for message in messages]
    self.storage_connection.lpush(self.name, *json_data)
      
  def deque(self , count :int= 1) -> dict:
    dequed_messages: List[str] = self.storage_connection.rpop(self.name , count)
    if not dequed_messages:
      return None
    
    dequed_messages = [json.loads(element) for element in dequed_messages]

    print(dequed_messages)
    logger.info(f"Dequed -> {dequed_messages}")
    return dequed_messages


  def continous_deque(self ,count = 1) -> Generator[List[dict],  None, None]:
    while True:
      dequed_element = self.deque(count=count)
      if dequed_element:
        yield dequed_element
      

  def deque_all(self) -> List[dict]:
    dequed_elements = []
    while True:
      dequed_element = self.deque()
      sleep(0.7)
      if not dequed_element:
        break
      print(dequed_element)
      logger.info(dequed_element)
      dequed_elements.append(dequed_element)
    return dequed_elements
  
    
class RedisList:
  def __init__(self, storage: RedisStorage, name: str) -> None:
    if not storage.connection:
      storage.connect()
        
    self.storage = storage
    self.name = name
    self.storage_connection:redis.Redis = storage.connection
    logger.info(f"connected to redis DB {self.storage_connection}")
    print(f"connected to redis DB {self.storage_connection}")
  def add_new(self,data :dict):
    json_data = json.dumps(data)
    logger.info(f"inserting {json_data}")
    print(f"inserting {json_data}")
    self.storage_connection.lpush(self.name , json_data)
      
  def retrieve_elements(self, count: int = 1)->List[dict]:
    retrieved_elements = self.storage_connection.lrange(
        name=self.name,
        start=0,
        end=count-1)

    formatted_elements = [json.loads(element) for element in retrieved_elements]
    
    logger.debug(f"retrieved -> {formatted_elements}")
    return formatted_elements
    