from enum import Enum


class PeerMark(Enum):
    CHAT = "CHAT"
    LOG = "LOG"


class UserPermission(Enum):
    user = 0
    moderator = 1
    administrator = 2


class SettingStatus(Enum):
    inactive = False
    active = True


class SettingDestination(Enum):
    filter = "filter"
    system = "system"


class UrlType(Enum):
    domain = "domain"
    url = "url"


class UrlStatus(Enum):
    forbidden = "forbidden"
    allowed = "allowed"


class StaffRole(Enum):
    ADM = "ADM"
    TECH = "TECH"
    SYS = "SYS"
