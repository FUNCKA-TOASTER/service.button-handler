"""Module "database".

File:
    connection.py

About:
    This module provides a utility function to build a
    connection URI for SQLAlchemy. The connection URI is
    constructed using the database setup configuration and
    credentials, allowing for secure and convenient connection
    string generation.
"""

from urllib.parse import quote
from toaster.credentials import AlchemySetup, AlchemyCredentials


def build_connection_uri(setup: AlchemySetup, creds: AlchemyCredentials) -> str:
    """Builds a SQLAlchemy connection URI from the provided setup and credentials.

    Args:
        setup (AlchemySetup): The configuration settings for the database connection.
        creds (AlchemyCredentials): The credentials required for the database connection.

    Returns:
        str: A formatted connection URI for SQLAlchemy.
    """

    return (
        f"{setup.dialect}+{setup.driver}://"
        f"{quote(creds.user)}:{quote(creds.pswd)}@"
        f"{creds.host}:{creds.port}/"
        f"{setup.database}"
    )
