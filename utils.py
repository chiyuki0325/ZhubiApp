from pyrogram.types import (
    User as PyrogramUser
)
import hmac
from hashlib import sha256
from functools import lru_cache
import random


def get_attr(some_object, attr):
    # 从某个可能为 None 的对象里获取属性
    if some_object is not None:
        return getattr(some_object, attr)
    else:
        return None


def get_member_name(member: PyrogramUser | None) -> str | None:
    def str_nullable(some_str_or_none: str | None) -> str:
        return some_str_or_none if some_str_or_none is not None else ''

    if member is None:
        return None
    return f"{str_nullable(member.first_name)} {str_nullable(member.last_name)}"


@lru_cache
def calculate_password_hash(password: str) -> str:
    return hmac.new(
        key='6634409710'.encode('utf-8'),
        msg=password.encode('utf-8'),
        digestmod=sha256
    ).hexdigest()


def generate_token() -> str:
    return random.randint(0, 2 ** 256).to_bytes(32, 'big').hex()

