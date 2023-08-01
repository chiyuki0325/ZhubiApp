# 外部模块
import importlib
from fastapi import APIRouter

router = APIRouter(
    prefix='/tg'
)

for router_module in [
    'chat', 'user'
]:
    router.include_router(
        importlib.import_module('routers.tg_routers.' + router_module).router
    )
