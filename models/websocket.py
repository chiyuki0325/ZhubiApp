# 借鉴自 https://github.com/purofle/webtg/blob/main/backend/model/websocket.py

from enum import IntEnum
from typing import Any

from pydantic import BaseModel


class Operations(IntEnum):
    # OP 怎么你了
    heartbeat = 0

    invalid_payload = 1000


class Payload(BaseModel):
    """
    Websocket 的负载。
    """
    operation_code: Operations = Operations.invalid_payload  # 操作代码
    data: Any = {}.copy()  # 数据
    sequence: int = 0  # 唯一 id

    class Config:
        fields = {
            "operation_code": "op",
            "data": "d",
            "sequence": "s"
        }
