
from pub_sub.storages.redis_controllers.controllers import RedisPublisher , RedisSubscriber , RedisStorage
import os

topic_name = os.getenv("TOPIC_NAME", "DEFAULT_TOPIC")
redis_host = os.getenv("REDIS_HOST", "redis")

storage = RedisStorage(host=redis_host)
storage.connect()

publisher = RedisPublisher(storage=storage, name=topic_name)
