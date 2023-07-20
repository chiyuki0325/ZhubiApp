# 借鉴自 https://github.com/purofle/webtg/blob/main/backend/routers/websocket.py

from typing import Any, Dict, Callable

from fastapi import WebSocket, APIRouter
from loguru import logger

from models.websocket import Payload, Operations

router = APIRouter(prefix="/websocket", tags=["websocket"])

event_handlers: Dict[int, Callable] = {}


def event(event_name):
    def decorator(func):
        event_handlers[event_name] = func
        return func

    return decorator


async def dispatch_event(
        op_code: int, websocket: WebSocket, *args, **kwargs
):
    handler_func = event_handlers.get(op_code)
    if handler_func is None:
        logger.error(f"找不到适用于事件 {op_code} 的处理程序")
        return
    await handler_func(websocket, *args, **kwargs)


@event(Operations.heartbeat)
async def op_ping(websocket: WebSocket, data: Any, seq: int):
    logger.info(str(data), seq)


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        # noinspection PyBroadException
        try:
            payload = Payload.model_validate(data)
        except Exception:
            await websocket.send_text(Payload(
                op_code=Operations.invalid_payload
            ).model_dump_json())
            await websocket.close()
            raise

        await dispatch_event(
            payload.operation_code,
            payload.data,
            payload.sequence
        )
