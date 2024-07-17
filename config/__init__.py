"""Module "config".

File:
    __init__.py

About:
    This file initializes the configuration variables
    used throughout the service. It imports and exposes
    key configuration constants such as API token,
    service name, and other settings required for proper
    operation.
"""

from .config import (
    REDIS_CREDS,  # Redis (broker) credentials
    CHANNEL_NAME,  # Broker subscription channel name
    TOKEN,  # API token
    GROUP_ID,  # ID of the group
    SERVICE_NAME,  # Name of the service
    API_VERSION,  # Version of the API
    ALCHEMY_SETUP,  # Setup for sqlalchemy. Driver, Database and DBMS.
    DBMS_CREDS,  # DBMS credentials includes host, port, user, password.
)


__all__ = (
    "REDIS_CREDS",
    "CHANNEL_NAME",
    "TOKEN",
    "GROUP_ID",
    "SERVICE_NAME",
    "API_VERSION",
    "ALCHEMY_SETUP",
    "DBMS_CREDS",
)
