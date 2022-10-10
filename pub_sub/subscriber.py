from storages.redis_controllers.controllers import RedisStorage, RedisSubscriber
import os

topic_name = os.getenv("TOPIC_NAME", "DEFAULT_TOPIC")

storage = RedisStorage()

publisher = RedisSubscriber(storage=storage, topic_name=topic_name)


def main():
    for data in publisher.listen():
        print ( data)
        
if __name__ == "__main__":
    main()