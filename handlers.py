# 消息处理器

# 外部模块
from pyrogram import Client
from pyrogram.types import Message as PyrogramMessage
from datetime import datetime
from loguru import logger

# 程序内模块
import context
from settings import settings
from database.access import DatabaseAccess

from database.models import (
    Chat,
    Message,
    User
)


async def client_message_handler(
        client: Client,
        message: PyrogramMessage
):
    async with context.db.async_session() as session:
        async with session.begin():
            da = DatabaseAccess(session)

            chat_id: int = message.chat.id

            chat: Chat | None = await da.get_chat_by_id(chat_id)
            if chat is None:
                # 保存聊天信息
                chat: Chat = await da.save_new_chat(message)

            message_obj: Message = await da.save_new_message(message)
            await da.touch_chat(chat, message_obj)  # 更新修改日期

            # 保存用户信息
            if message.from_user:
                user: User | None = await da.get_user_by_id(message.from_user.id)
                if user is None:
                    await da.save_new_user(message.from_user)
                else:
                    await da.touch_user(user, message)

