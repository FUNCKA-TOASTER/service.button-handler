from datetime import datetime
from toaster.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import (
    TINYINT,
    BIGINT,
    INTEGER,
    VARCHAR,
    DATETIME,
)
from .enums import (
    PeerMark,
    UserPermission,
    SettingDestination,
    SettingStatus,
    UrlStatus,
    UrlType,
    StaffRole,
)

from .annotated import UUID, BPID


# TODO: Прописать ondelete в местах, где это нужно
# Таблицы основных элементов
class Peer(BaseModel):
    __tablename__ = "peers"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    mark: Mapped[PeerMark]


# Таблицы данных о пользователе и сообщениях
class Permission(BaseModel):
    __tablename__ = "permissions"

    bpid: Mapped[BPID]
    uuid: Mapped[UUID]
    permission: Mapped[UserPermission]


class Warn(BaseModel):
    __tablename__ = "warns"

    bpid: Mapped[BPID]
    uuid: Mapped[UUID]
    points: Mapped[int] = mapped_column(TINYINT(10))
    expired: Mapped[datetime] = mapped_column(DATETIME)


class Session(BaseModel):
    __tablename__ = "sessions"

    bpid: Mapped[BPID]
    cmid: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    expired: Mapped[datetime] = mapped_column(DATETIME)


class Queue(BaseModel):
    __tablename__ = "queues"

    bpid: Mapped[BPID]
    uuid: Mapped[UUID]
    expired: Mapped[int] = mapped_column(DATETIME)


# Таблицы настроект узлов
class Setting(BaseModel):
    __tablename__ = "settings"

    bpid: Mapped[BPID]
    name: Mapped[str] = mapped_column(VARCHAR(30), primary_key=True)
    status: Mapped[SettingStatus]
    destination: Mapped[SettingDestination]
    points: Mapped[int] = mapped_column(TINYINT(10))


class Cursed(BaseModel):
    __tablename__ = "curses"

    bpid: Mapped[BPID]
    word: Mapped[str] = mapped_column(VARCHAR(40), primary_key=True)


class Delay(BaseModel):
    __tablename__ = "delays"

    bpid: Mapped[BPID]
    setting: Mapped[str] = mapped_column(VARCHAR(30), primary_key=True)
    delay: Mapped[int] = mapped_column(INTEGER)


class Url(BaseModel):
    __tablename__ = "urls"

    bpid: Mapped[BPID]
    type: Mapped[UrlType] = mapped_column(primary_key=True)
    pattern: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    status: Mapped[UrlStatus]


class Staff(BaseModel):
    __tablename__ = "staffs"

    uuid: Mapped[UUID]
    role: Mapped[StaffRole]
