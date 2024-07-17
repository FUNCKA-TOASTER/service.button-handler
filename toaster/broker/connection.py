"""Module "broker".

File:
    connection.py

About:
    This module provides functionality to build a
    connection to a Redis server. It includes a function
    that takes Redis credentials and returns a Redis
    connection object.
"""

from redis import Redis
from toaster.credentials import RedisCredentials


def build_connection(creds: RedisCredentials) -> Redis:
    """Builds and returns a Redis connection object.

    Args:
        creds (RedisCredentials): The credentials required to connect to the Redis.

    Returns:
        Redis: A Redis connection object.
    """

    return Redis(
        host=creds.host,
        port=creds.port,
        db=creds.db,
    )
