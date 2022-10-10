
from .storages.redis_controllers.controllers import RedisStorage, RedisQueue
import os

topic_name = os.getenv("TOPIC_NAME", "DEFAULT_TOPIC")
redis_host = os.getenv("REDIS_HOST", "redis")

storage = RedisStorage(host=redis_host)
storage.connect()

local_queue = RedisQueue(storage=storage, name=topic_name)


def get_new_redis_queue(name :str)->RedisQueue:
    return RedisQueue(storage=storage, name=name)




