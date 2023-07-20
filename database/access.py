# SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from pyrogram.types import (
    Message as PyrogramMessage
)
from pyrogram.enums import (
    MessageMediaType
)

# 程序内模块
from database.models import (
    Chat,
    Message,
    User,
    MessageType,
    UnsupportedMessageType,
    SystemMessageType,
    Sticker
)
from utils import get_member_name, get_attr


class DatabaseAccess:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def flush(self):
        await self.session.flush()

    async def get_chat_by_id(self, id: int) -> Chat | None:
        # 在接收到新消息时获取聊天对象
        chat: Chat | None = (await self.session.execute(
            select(Chat).where(Chat.id == id)
        )).scalars().first()
        return chat

    async def save_new_chat(self, message: PyrogramMessage) -> Chat:
        # 在第一次接收到来自某个聊天的消息时
        # 在数据库中创建聊天对象
        chat = Chat(
            id=message.chat.id,
            type=message.chat.type,
            title=message.chat.title,
            username=message.chat.username,
            last_updated=datetime.now(),
            last_message_db_id=None,
            pinned=False,
            photo_file_id=get_attr(message.chat.photo, 'big_file_id')
        )
        self.session.add(chat)
        await self.flush()
        return chat

    async def touch_chat(self, chat: Chat, message: PyrogramMessage):
        # 更新 chat 的修改日期和最新消息
        chat.last_updated = datetime.now()
        chat.last_message_db_id = message.id
        self.session.add(chat)
        await self.flush()

    async def save_new_message(self, message: PyrogramMessage) -> Message:
        # 接收到新消息时，存储到数据库
        message_type = MessageType.unsupported
        system_message_type = SystemMessageType.other
        unsupported_type = UnsupportedMessageType.other
        system_message: str | None = None
        sticker: dict | None = None
        if message.media is not None:
            if (message.photo is not None) or (message.media == MessageMediaType.PHOTO):
                # 图片
                message_type = MessageType.photo
            elif (message.sticker is not None) or (message.media == MessageMediaType.STICKER):
                # 贴纸
                message_type = MessageType.sticker
                sticker_obj = Sticker()
                sticker_obj.file_id = message.sticker.file_id
                sticker_obj.emoji = message.sticker.emoji
                sticker = sticker_obj.model_dump(mode='json')
            else:
                # 不支持的消息类型
                message_type = MessageType.unsupported
                match message.media:
                    case MessageMediaType.VIDEO | MessageMediaType.VIDEO_NOTE:
                        unsupported_type = UnsupportedMessageType.video
                    case MessageMediaType.ANIMATION:
                        unsupported_type = UnsupportedMessageType.animation
                    case MessageMediaType.GAME:
                        unsupported_type = UnsupportedMessageType.game
                    case MessageMediaType.POLL:
                        unsupported_type = UnsupportedMessageType.poll
                    case MessageMediaType.VOICE:
                        unsupported_type = UnsupportedMessageType.voice
                    case MessageMediaType.AUDIO:
                        unsupported_type = UnsupportedMessageType.audio
        elif message.new_chat_title is not None:
            # 设置了新群名
            chat = await self.get_chat_by_id(message.chat.id)
            chat.title = message.new_chat_title
            self.session.add(chat)
            message_type = MessageType.system
            system_message_type = SystemMessageType.new_chat_title
        elif message.new_chat_photo is not None:
            # 设置了新群头像
            chat = await self.get_chat_by_id(message.chat.id)
            chat.photo_file_id = message.new_chat_photo.file_id
            self.session.add(chat)
            message_type = MessageType.system
            system_message_type = SystemMessageType.new_chat_photo
        elif message.new_chat_members is not None:
            # 新成员加入
            system_message = ', '.join(
                map(
                    lambda member: get_member_name(member),
                    message.new_chat_members
                )
            )
            message_type = MessageType.system
            system_message_type = SystemMessageType.new_member
        elif message.left_chat_member is not None:
            # 成员退出
            system_message = get_member_name(message.left_chat_member)
            message_type = MessageType.system
            system_message_type = SystemMessageType.left_member
        else:
            if message.text is not None:
                if message.text != '':
                    message_type = MessageType.text

        message = Message(
            tg_id=message.id,
            type=message_type,
            unsupported_type=unsupported_type,
            sender_id=get_attr(message.user, 'id'),
            sender_chat_id=get_attr(message.sender_chat, 'id'),
            chat_id=message.chat.id,
            send_at=message.date,
            text=get_attr(message.text, 'markdown'),
            caption=get_attr(message.caption, 'markdown'),
            mentioned=bool(message.mentioned),
            title=message.author_signature,
            sticker=sticker,
            photo_id=get_attr(message.photo, 'file_id'),
            photo_spoiler=bool(message.has_media_spoiler),
            system_message_type=system_message_type,
            system_message=system_message,
            outgoing=bool(message.outgoing),
            reply_to_tg_id=message.reply_to_message_id,
            forward_from_user_name=get_member_name(message.forward_from),
            via_bot_username=get_attr(message.via_bot, 'username'),
            forward_from_chat_name=get_attr(message.forward_from_chat, 'title')
        )
        self.session.add(message)
        await self.flush()
