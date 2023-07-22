# 借鉴自 https://github.com/purofle/webtg/blob/main/backend/routers/websocket.py

from typing import Any, Dict, Callable
from functools import wraps
from datetime import datetime

from fastapi import APIRouter
from loguru import logger
import rapidjson as json

# 要开始从 starlette 层面下手了
from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint
import broadcaster

from models.websocket import Payload, Operations
import context
from settings import settings

router = APIRouter(prefix="/ws", tags=["websocket"])

event_handlers: Dict[int, Callable] = {}


@router.websocket_route("/", name="ws")
# http://localhost:5586/ws/
class ZhubiWebSocket(WebSocketEndpoint):
    encoding = 'text'

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()

    async def on_receive(self, websocket: WebSocket, data: str):
        try:
            payload = Payload.model_validate(
                json.loads(data)
            )
        except Exception:
            await websocket.send_text(Payload(
                op_code=Operations.invalid_payload
            ).model_dump_json(by_alias=True))
            await websocket.close()
            raise

        await dispatch_event(
            operation_code=payload.operation_code,
            websocket=websocket,
            data=payload.data,
            token=payload.token
        )

    async def on_disconnect(self, websocket, close_code):
        pass


def event(event_name):
    def decorator(func):
        event_handlers[event_name] = func
        return func

    return decorator


def needs_token(func):
    @wraps(func)
    async def wrapper(websocket: WebSocket, data: Any, token: str = ""):
        if context.token is None:
            msg = "尚未登录"
        elif context.token != token:
            msg = "token 不匹配"
        elif (datetime.now() - context.token_last_used).total_seconds() / 60 > settings.token_expire_minutes:
            msg = "登录已过期"
        else:
            return await func(websocket, data, token)
        await websocket.send_text(Payload(
            operation_code=Operations.invalid_payload,
            data={"msg": msg}
        ).model_dump_json(by_alias=True))
        await websocket.close()
        return

    return wrapper


@event(Operations.heartbeat)
@event(Operations.ping)
async def op_ping(websocket: WebSocket, data: Any, token: str):
    await websocket.send_text(Payload(
        operation_code=Operations.pong,
    ).model_dump_json(by_alias=True))


async def dispatch_event(
        operation_code: int,
        websocket: WebSocket,
        data: Any,
        token: str,
):
    handler_func = event_handlers.get(operation_code)
    if handler_func is None:
        logger.error(f"找不到适用于事件 {operation_code} 的处理程序")
        return
    await handler_func(websocket, data, token)
