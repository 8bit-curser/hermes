from enum import Enum


class UserTypeEnum(Enum):
    client = 1
    provider = 2
    admin = 10


class RequestStateEnum(Enum):
    ready = 2
    sent = 3
    done = 1
    fail = 0


