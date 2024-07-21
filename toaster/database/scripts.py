"""Module "database".

File:
    scripts.py

About:
    This module provides a decorator for marking
    functions as custom scripts for SQLAlchemy.
    The `script` decorator facilitates the execution
    of database operations within a managed session,
    with options for automatic commit and debugging.
    It simplifies the process of writing and calling
    scripts that interact with the database by encapsulating
    session management and error handling.
"""

from typing import Callable, Optional, Any
from loguru import logger
from .database import Database


def script(auto_commit: bool = True, debug: bool = False) -> Callable:
    """A decorator that implements a custom script wrapper.

    The decorator allows you to mark a function
    as a custom script for sqlalchemy. Using
    this mechanism, you can conveniently call
    the desired set of actions in the right place.
    It is enough only to transfer the instance of
    the database class to the script.

    Example: ::

        @script(auto_commit=False)
        def add_user(session: Session, name: str, age: int):
            new_user = User(name=name, age=age)
            session.add(new_user)
            session.commit()

        @script(auto_commit=False)
        def ge_user(session: Session, id: int):
            user = session.get(User, {"id": id})
            return user

        # But calling requires Database instance
        add_user(db, name="Vasya", age=15)
        get_user(db, id=25611)
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(db_instance: Database, *args, **kwargs) -> Optional[Any]:
            session = db_instance.make_session()
            try:
                result = func(session, *args, **kwargs)

                if auto_commit:
                    session.commit()

                return result

            except Exception as error:
                session.rollback()

                if debug:
                    _handle_exception(error, func)

            finally:
                session.close()

        return wrapper

    return decorator


def _handle_exception(error: Exception, func: Callable) -> None:
    text = (
        f"Script <{func.__name__}> execution failed. "
        "Transaction rolled back. \n"
        f"ErrorMessage: {error}"
    )
    logger.error(text)
