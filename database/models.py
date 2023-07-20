from database.database import Base
from sqlalchemy import Column as Col
from sqlalchemy import Integer, UnicodeText, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import (
    ARRAY as Array,
    JSON as Json
)
from enum import Enum as PythonEnum
from sqlalchemy import Enum as ColEnum

from pydantic import BaseModel
from typing import Optional

from pyrogram.enums import ChatType, UserStatus


class Chat(Base):
    __tablename__ = "chats"
    id = Col(Integer, primary_key=True)

    type = Col(ColEnum(ChatType))

    title = Col(UnicodeText)
    username = Col(UnicodeText, nullable=True)

    last_updated = Col(DateTime)
    # 若不特别说明，id 均指数据库中的 id
    last_message_id = Col(Integer)

    pinned = Col(Boolean, default=False)


class User(Base):
    __tablename__ = "users"
    id = Col(Integer, primary_key=True)

    is_bot = Col(Boolean, default=False)
    is_premium = Col(Boolean, default=False)

    first_name = Col(UnicodeText, nullable=True)
    last_name = Col(UnicodeText, nullable=True)
    username = Col(UnicodeText, nullable=True)

    # 电话号
    box = Col(UnicodeText, nullable=True)

    photo_file_id = Col(Text, nullable=True)
    status = Col(ColEnum(UserStatus), nullable=True)
    last_online = Col(DateTime, nullable=True)


class MessageType(PythonEnum):
    text = 0
    photo = 1
    photo_with_caption = 2
    sticker = 3
    mixed = 4
    system = 5
    unsupported = 9


class SystemMessageType(PythonEnum):
    new_member = 0
    change_photo = 1
    unsupported_or_other = 9


class Sticker(BaseModel):
    file_id: str
    emoji: str


class Message(Base):
    __tablename__ = "messages"
    id = Col(Integer, primary_key=True)

    type = Col(ColEnum(MessageType))

    sender_id = Col(Integer, nullable=True)
    chat_id = Col(Integer, nullable=True)
    send_at = Col(DateTime, nullable=True)

    text = Col(UnicodeText, nullable=True)  # 存储 markdown 文本
    caption = Col(UnicodeText, nullable=True)
    mentioned = Col(Boolean, default=False)
    title = Col(UnicodeText, nullable=True)  # 头衔

    sticker = Col(Json, nullable=True)
    photo_id = Col(Text, nullable=True)
    photo_spoiler = Col(Boolean, default=False)

    system_message_type = Col(ColEnum(SystemMessageType))
    system_message = Col(UnicodeText, nullable=True)

    outgoing = Col(Boolean, default=False)
    reply_to = Col(Integer, nullable=True)

    # 转发消息的来源直接摆烂做成不可点击
    forward_from_user_name = Col(UnicodeText, nullable=True)
    forward_from_chat_id = Col(Integer, nullable=True)
