from app.mailer.sendmail import send_mail_notification
from pub_sub.storages.redis_controllers.controllers import RedisList
from pub_sub.queues import local_queue


def enque_by_user():

  current_users = {}

  for messages in local_queue.continous_deque(count=100):
    for message in messages:

      subscribers_id = message['subscribers_id']

      for user_id in subscribers_id:

        front_page_list_name = f"front_page_user_{user_id}"

        if front_page_list_name not in current_users:
            current_users[front_page_list_name] = RedisList(
                storage=local_queue.storage,
                name=front_page_list_name
            )
        curren_user_list: RedisList = current_users[front_page_list_name]
        curren_user_list.add_new(data=message["message"])


def send_mail_deque_service():
  for message in local_queue.continous_deque(count=5):
    for single_message in message:
      send_mail_notification(**single_message)


TOPIC_ACTIONS = {
    "MAILER": send_mail_notification,
    "ENQUE_BY_USER": enque_by_user
}
