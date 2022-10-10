from typing import Callable
from .queues import topic_name
from queue_actions.actions import TOPIC_ACTIONS


def main():
    current_action: Callable = TOPIC_ACTIONS.get(topic_name)

    current_action()


if __name__ == "__main__":

    main()
