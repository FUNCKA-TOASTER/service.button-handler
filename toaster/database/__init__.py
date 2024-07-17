"""Module "database".

File:
    __init__.py

About:
    This file serves as the entry point for the 'database' package,
    providing convenient access to functionalities related to database
    connections, script execution, and ORM models.
"""

from .connection import build_connection_uri
from .database import Database, BaseModel
from .scripts import script


__all__ = (
    "build_connection_uri",  # A function to build SQLAlchemy connection URIs.
    "script",  # A decorator to mark functions as custom scripts for SQLAlchemy.
    "Database",  # Class encapsulating SQLAlchemy database management operations.
    "BaseModel",  # Base class for SQLAlchemy models.
)
