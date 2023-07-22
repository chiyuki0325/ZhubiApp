# 借鉴自 https://github.com/purofle/webtg/blob/main/backend/model/websocket.py

from enum import IntEnum
from typing import Any

from pydantic import BaseModel, Field


class Operations(IntEnum):
    # OP 怎么你了
    heartbeat = 0  # 每 30 秒一次
    ping = 1  # 刚连接上时发送一次
    pong = 2  # 服务器返回
    new_message = 3  # 接收到新消息

    invalid_payload = 1000


class Payload(BaseModel):
    """
    Websocket 的负载。
    """
    operation_code: Operations = Field(default=Operations.invalid_payload, alias="op")
    data: Any = Field(default={}.copy(), alias="d")
    token: str = Field(default="", alias="t")
