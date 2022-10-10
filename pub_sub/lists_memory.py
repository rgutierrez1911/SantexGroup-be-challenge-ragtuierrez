
from .storages.redis_controllers.controllers import RedisStorage, RedisList
import os

topic_name = os.getenv("TOPIC_NAME", "DEFAULT_TOPIC")
redis_host = os.getenv("REDIS_HOST", "redis")

storage = RedisStorage(host=redis_host)
storage.connect()




def get_new_redis_list(name :str)->RedisList:
    return RedisList(storage=storage, name=name)

