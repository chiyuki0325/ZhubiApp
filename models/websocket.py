# 借鉴自 https://github.com/purofle/webtg/blob/main/backend/model/websocket.py

from enum import IntEnum
from typing import Any

from pydantic import BaseModel, Field


class Operations(IntEnum):
    # OP 怎么你了
    heartbeat = 0
    ping = 1
    pong = 2

    invalid_payload = 1000


class Payload(BaseModel):
    """
    Websocket 的负载。
    """
    operation_code: Operations = Field(default=Operations.invalid_payload, alias="op")
    data: Any = Field(default={}.copy(), alias="d")
    token: str = Field(default="", alias="t")
