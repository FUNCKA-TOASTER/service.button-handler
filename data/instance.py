"""В этом файле отписываются коннекты к базама данных, схемамам и т.д."""

from toaster.database import Database, build_connection_uri
from config import ALCHEMY_SETUP, DBMS_CREDS


# Инстанция базы данных
TOASTER_DB = Database(build_connection_uri(ALCHEMY_SETUP, DBMS_CREDS))

# TODO: Translate to eng
