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

    id = Col(Integer, primary_key=True)  # tg id

    type = Col(ColEnum(ChatType))  # 聊天类型
    title = Col(UnicodeText)  # 群聊：群名，私聊：对方名字
    username = Col(UnicodeText, nullable=True)  # username，可能为空
    photo_file_id = Col(Text, nullable=True)  # 头像 file_id

    last_updated = Col(DateTime)  # 最后一次消息的时间
    # 若不特别说明，id 均指 tg id
    last_message_db_id = Col(Integer, nullable=True)  # 最后一条消息的数据库 id

    pinned = Col(Boolean, default=False)  # 是否置顶


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id = Col(Integer, primary_key=True)  # tg id

    is_bot = Col(Boolean, default=False)  # 是否为 bot
    is_premium = Col(Boolean, default=False)  # 是否为大会员

    first_name = Col(UnicodeText, nullable=True)
    last_name = Col(UnicodeText, nullable=True)
    username = Col(UnicodeText, nullable=True)

    box = Col(UnicodeText, nullable=True)  # 电话号

    photo_file_id = Col(Text, nullable=True)  # 头像 file_id
    status = Col(ColEnum(UserStatus), nullable=True)  # 在线状态
    last_online = Col(DateTime, nullable=True)  # 最后一次在线时间(如果设为公开)


class MessageType(PythonEnum):
    text = 0  # 纯文本
    photo = 1  # 带图
    sticker = 3  # 贴纸
    system = 5  # 系统消息（显示为灰色条）
    unsupported = 9  # 不支持的消息类型（如果有 system_message 字段，就显示为正常消息）


class UnsupportedMessageType(PythonEnum):
    # 不支持的消息类型将会依据 UnsupportedMessageType 尽可能转换为文本消息
    # 转换的结果存储在 system_message 字段中
    animation = 0
    game = 1
    video = 2
    voice = 3
    audio = 4
    poll = 5
    file = 6
    other = 9


class SystemMessageType(PythonEnum):
    new_member = 0
    new_chat_photo = 1
    new_chat_title = 2
    left_member = 3
    other = 9  # 直接展示 system_message 字段


class Sticker(BaseModel):
    file_id: str
    emoji: Opt[str]  # 🥰


class Message(Base):
    __tablename__ = "messages"
    __mapper_args__ = {"eager_defaults": True}

    id = Col(Integer, primary_key=True)  # 数据库 id
    tg_id = Col(Integer)  # tg id

    type = Col(ColEnum(MessageType))  # 消息类型(自己定义的)
    unsupported_type = Col(ColEnum(UnsupportedMessageType))  # 如果是不支持的消息类型，将会尽可能转换为文本消息

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
    system_message = Col(UnicodeText, nullable=True)
    # 可能是新加入的用户们，也可能是被飞掉的用户
    # 还可能是转换后的不支持的消息

    outgoing = Col(Boolean, default=False)
    reply_to_tg_id = Col(Integer, nullable=True)

    # 转发消息的来源直接摆烂做成不可点击
    forward_from_user_name = Col(UnicodeText, nullable=True)
    forward_from_chat_name = Col(UnicodeText, nullable=True)
    via_bot_username = Col(Text, nullable=True)

    deleted = Col(Boolean, default=False)  # 是否被删除
