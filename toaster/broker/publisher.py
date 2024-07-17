"""Module "broker".

File:
    publisher.py

About:
    This file contains the implementation of the
    Publisher class, which facilitates publishing
    serialized objects to Redis channels. It provides
    methods for initializing the Redis client, serializing
    objects, and publishing them to specified channels.
"""

from typing import ByteString, Any
import dill as pickle
from redis import Redis
from loguru import logger


class Publisher:
    """Initializes the Publisher with a Redis client.

    Description:
        Class for publishing serialized objects to Redis channels.

    """

    def __init__(self, client: Redis) -> None:
        self.client = client

    # TODO: handle possible exeptions
    def publish(self, obj: Any, channel_name: str) -> int:
        """Publishes a serialized object to a Redis channel.

        Args:
            obj (object): Object to be serialized and published.
            channel_name (str): Name of the Redis channel to publish to.

        Returns:
            int: Status code indicating the result of the publish operation.
        """

        logger.info(f"Sending object: {obj}")
        data = self.__serialize(obj)
        status = self.client.publish(channel_name, data)

        return status

    @staticmethod
    def __serialize(obj: Any) -> ByteString:
        return pickle.dumps(obj=obj, protocol=pickle.HIGHEST_PROTOCOL)
