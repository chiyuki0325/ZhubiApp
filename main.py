#!/usr/bin/env python3

# web 服务
from fastapi import FastAPI
import uvloop
import uvicorn

# Telegram
from pyrogram import Client
from pyrogram.handlers import MessageHandler

# 程序内模块
import context
from settings import settings, app_version
from database.database import Database
from handlers import client_message_handler

# 外部模块
import os
from loguru import logger
import logging
import richuru

api = FastAPI()


# noinspection PyUnresolvedReferences
@api.on_event('startup')
async def startup_event():
    # 初始化日志
    logging.getLogger('pyrogram').setLevel(settings.loglevel)
    richuru.install(level=settings.loglevel)

    # 初始化客户端
    context.client = Client(
        'zhubiapp',
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
        app_version='ZhubiApp ' + app_version,
    )
    context.client.add_handler(
        MessageHandler(client_message_handler)
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
