"""Service "session.button-handler".

File:
    start.py

About:
    This service is responsible for receiving custom
    events from the Redis channel "button", processing
    these events, and executing actions based on the
    button action name specified in the payload.
"""

import sys
from loguru import logger
from funcka_bots.broker import Subscriber
from handler import ButtonHandler
import config


def setup_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <red>{module}</red> | <level>{level}</level> | {message}",
        level="DEBUG",
    )


def main():
    """Programm entry point."""

    setup_logger()
    subscriber = Subscriber(creds=config.BROKER_CREDS)
    handler = ButtonHandler()

    for event in subscriber.listen(queue_name=config.BROKER_QUEUE_NAME):
        handler(event)


if __name__ == "__main__":
    main()
