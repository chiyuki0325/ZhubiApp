#!/usr/bin/env python3

# web 服务
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvloop
import uvicorn
from broadcaster import Broadcast

# Telegram
from pyrogram import Client
from pyrogram.handlers import (
    MessageHandler,
    DeletedMessagesHandler
)

# 程序内模块
import context
from settings import settings, app_version, Settings
from database.database import Database
from handlers import *

# 外部模块
import os
from loguru import logger
import logging
import richuru
import importlib

api = FastAPI()

for router_module in [
    'misc', 'user', 'websocket'
]:
    api.include_router(
        importlib.import_module('routers.' + router_module).router
    )
api.mount(
    '/',
    StaticFiles(
        directory=settings.frontend_files,
        html=True
    ),
    name='frontend'
)
api.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins.split(','),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@api.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return FileResponse(
        os.path.join(settings.frontend_files, 'index.html')
    )


def check_settings(_settings: Settings) -> bool:
    if _settings.auth_method not in [
        'password', 'webauthn'
    ]:
        logger.error(
            '配置文件中的 auth_method 参数不正确，请检查配置文件。\n'
            '目前支持 password 或 webauthn。',
            style='bold red'
        )
        return False
    return True


# noinspection PyUnresolvedReferences
@api.on_event('startup')
async def startup_event():
    # 初始化日志
    logging.getLogger('pyrogram').setLevel(settings.loglevel)
    richuru.install(level=settings.loglevel)

    # 检查配置文件
    if not check_settings(settings):
        logger.error(
            '配置文件检查失败，请检查配置文件是否正确。',
            style='bold red'
        )
        exit(1)

    # 初始化客户端
    context.client = Client(
        'zhubiapp',
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
        app_version='ZhubiApp ' + app_version,
    )
    # 添加消息处理器
    context.client.add_handler(
        MessageHandler(client_message_handler)
    )
    context.client.add_handler(
        DeletedMessagesHandler(client_message_deletion_handler)
    )
    api.state.client = context.client

    # 连接数据库
    logger.info(
        '正在连接数据库 ...'
    )
    context.db = Database()
    await context.db.create_columns()
    api.state.db = context.db

    # 登录流程
    if not os.path.exists('zhubiapp.session'):
        logger.info(
            '您是第一次运行 ZhubiApp，进入 Pyrogram 登录流程。',
            style='bold yellow'
        )

    await context.client.start()


def main():
    uvloop.install()
    uvicorn.run(
        app=api,
        host=settings.api_host,
        port=settings.api_port
    )


if __name__ == '__main__':
    main()
