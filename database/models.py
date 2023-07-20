# 此文件中定义着数据结构

from database.database import Base
from sqlalchemy import (
    Column as Col,
    BigInteger as Integer,
    Enum as ColEnum
)
from sqlalchemy import UnicodeText, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import (
    JSON as Json
)
from enum import Enum as PythonEnum
from pydantic import BaseModel
from typing import Optional as Opt
from pyrogram.enums import ChatType, UserStatus


class Chat(Base):
    __tablename__ = "chats"
    __mapper_args__ = {"eager_defaults": True}

    id = Col(Integer, primary_key=True)

    type = Col(ColEnum(ChatType))

    title = Col(UnicodeText)
    username = Col(UnicodeText, nullable=True)
    photo_file_id = Col(Text, nullable=True)

    last_updated = Col(DateTime)
    # 若不特别说明，id 均指 tg id
    last_message_db_id = Col(Integer, nullable=True)

    pinned = Col(Boolean, default=False)


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

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
    sticker = 3
    system = 5
    unsupported = 9


class UnsupportedMessageType(PythonEnum):
    animation = 0
    game = 1
    video = 2
    voice = 3
    audio = 4
    poll = 5
    other = 9


class SystemMessageType(PythonEnum):
    new_member = 0
    new_chat_photo = 1
    new_chat_title = 2
    left_member = 3
    other = 9


class Sticker(BaseModel):
    file_id: str
    emoji: Opt[str]


class Message(Base):
    __tablename__ = "messages"
    __mapper_args__ = {"eager_defaults": True}

    id = Col(Integer, primary_key=True)
    tg_id = Col(Integer)

    type = Col(ColEnum(MessageType))
    unsupported_type = Col(ColEnum(UnsupportedMessageType))

    sender_id = Col(Integer, nullable=True)  # tg id，也是数据库 id
    sender_chat_id = Col(Integer, nullable=True)
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
    system_message = Col(UnicodeText, nullable=True)  # 可能是新加入的用户们，也可能是被飞掉的用户

    outgoing = Col(Boolean, default=False)
    reply_to_tg_id = Col(Integer, nullable=True)

    # 转发消息的来源直接摆烂做成不可点击
    forward_from_user_name = Col(UnicodeText, nullable=True)
    forward_from_chat_name = Col(UnicodeText, nullable=True)
    via_bot_username = Col(Text, nullable=True)

