# 数据访问组件

# 外部模块
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from pyrogram.types import (
    Message as PyrogramMessage,
    User as PyrogramUser,
)
from pyrogram.enums import (
    MessageMediaType
)
from loguru import logger
from typing import Optional as Opt

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

    async def get_chat_by_id(self, chat_id: int) -> Chat | None:
        # 在接收到新消息时获取聊天对象
        chat: Chat | None = (await self.session.execute(
            select(Chat).where(Chat.id == chat_id)
        )).scalars().first()
        return chat

    async def save_new_chat(self, message: PyrogramMessage) -> Chat:
        # 在第一次接收到来自某个聊天的消息时
        # 在数据库中创建聊天对象
        logger.info(
            f'创建新的聊天对象: {message.chat.id} {message.chat.type} {message.chat.title} {message.chat.username}',
            alt=f'[bold]创建新的聊天对象[/]: {message.chat.id} {message.chat.type} {message.chat.title} {message.chat.username}'
        )
        if message.chat.title is not None:
            # 群聊
            title = message.chat.title
        else:
            # 私聊
            # noinspection PyBroadException
            try:
                title = get_member_name(message.from_user)
            except Exception:
                title = message.from_user.username
        chat = Chat(
            id=message.chat.id,
            type=message.chat.type,
            title=title,
            username=message.chat.username,
            last_updated=datetime.now(),
            last_message_db_id=None,
            pinned=False,
            photo_file_id=get_attr(message.chat.photo, 'big_file_id')
        )
        self.session.add(chat)
        await self.flush()
        return chat

    async def touch_chat(self, chat: Chat, message: Opt[PyrogramMessage | None] = None):
        # 更新 chat 的修改日期和最新消息
        chat.last_updated = datetime.now()
        if message is not None:
            chat.last_message_db_id = message.id
        self.session.add(chat)
        await self.flush()

    async def save_new_message(self, message: PyrogramMessage) -> Message | None:
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
                sticker_obj = Sticker(
                    file_id=message.sticker.file_id,
                    emoji=message.sticker.emoji
                )
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
                        system_message = '[游戏]' + message.game.title + '\n' + message.game.description
                    case MessageMediaType.POLL:
                        unsupported_type = UnsupportedMessageType.poll
                        system_message = '[投票]' + message.poll.question
                        for option in message.poll.options:
                            system_message += '\n- ' + option.text
                    case MessageMediaType.VOICE:
                        unsupported_type = UnsupportedMessageType.voice
                        if message.voice.duration:
                            system_message = f'[语音] ({message.voice.duration} 秒)'
                    case MessageMediaType.AUDIO:
                        unsupported_type = UnsupportedMessageType.audio
                        if message.audio.title:
                            system_message = message.audio.title
                        elif message.audio.file_name:
                            system_message = message.audio.file_name
                        else:
                            system_message = '[音频文件]'
                    case MessageMediaType.WEB_PAGE:
                        # 不存
                        return
                    case MessageMediaType.DOCUMENT:
                        unsupported_type = UnsupportedMessageType.file
                        # 文件
                        if message.document.file_name:
                            system_message = message.document.file_name
                        else:
                            system_message = '[' + message.document.mime_type + ' 文件]'
        elif message.new_chat_title is not None:
            # 设置了新群名
            chat = await self.get_chat_by_id(message.chat.id)
            chat.title = message.new_chat_title
            self.session.add(chat)
            message_type = MessageType.system
            system_message_type = SystemMessageType.new_chat_title
            logger.info(
                f'{chat.title} 设置了新群名',
                alt=f'[bold magenta]{chat.title} 设置了新群名[/]'
            )
        elif message.new_chat_photo is not None:
            # 设置了新群头像
            chat = await self.get_chat_by_id(message.chat.id)
            chat.photo_file_id = message.new_chat_photo.file_id
            self.session.add(chat)
            message_type = MessageType.system
            system_message_type = SystemMessageType.new_chat_photo
            logger.info(
                f'{message.chat.title} 设置了新群头像',
                alt=f'[bold magenta]{message.chat.title} 设置了新群头像[/]'
            )
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
            logger.info(
                f'新成员加入 {message.chat.title}: '
                f'{system_message}',
                alt=f'[bold magenta]新成员加入 {message.chat.title}[/]: '
                    f'{system_message}'
            )
        elif message.left_chat_member is not None:
            # 成员退出
            system_message = get_member_name(message.left_chat_member)
            message_type = MessageType.system
            system_message_type = SystemMessageType.left_member
            logger.info(
                f'成员退出 {message.chat.title}: '
                f'{get_member_name(message.left_chat_member)} ({message.left_chat_member.username})',
                alt=f'[bold magenta]成员退出 {message.chat.title}[/]: '
                    f'{get_member_name(message.left_chat_member)} ({message.left_chat_member.username})'
            )
        else:
            if message.text is not None:
                if message.text != '':
                    message_type = MessageType.text
        logger.info(
            f'收到新消息: {message.id} ({message_type.name}) {message.text} - '
            f'来自聊天 {message.chat.title} 中的 {get_member_name(message.from_user)}',
            alt=f'[bold]收到新消息[/]: {message.id} ({message_type.name}) - '
                f'来自聊天 {message.chat.title} 中的 {get_member_name(message.from_user)}'
        )
        message = Message(
            tg_id=message.id,
            type=message_type,
            unsupported_type=unsupported_type,
            sender_id=get_attr(message.from_user, 'id'),
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
            forward_from_chat_name=get_attr(message.forward_from_chat, 'title'),
            deleted=False
        )
        self.session.add(message)
        await self.flush()
        return message

    async def get_user_by_id(self, user_id: int) -> User | None:
        # 获取用户对象
        user: User | None = (await self.session.execute(
            select(User).where(User.id == user_id)
        )).scalars().first()
        return user

    async def save_new_user(self, user: PyrogramUser) -> User:
        user: User = User(
            id=user.id,
            username=user.username,
            is_bot=bool(user.is_bot),
            is_premium=bool(user.is_premium),
            first_name=user.first_name,
            last_name=user.last_name,
            box=user.phone_number,
            photo_file_id=get_attr(user.photo, 'big_file_id'),
            status=user.status,
            last_online=user.last_online_date,
        )
        self.session.add(user)
        await self.flush()
        return user

    async def touch_user(self, user: User, message: PyrogramMessage):
        # 更新 user 的状态
        user.status = message.from_user.status
        user.last_online = message.from_user.last_online_date
        if user.first_name != message.from_user.first_name:
            user.first_name = message.from_user.first_name
        if user.last_name != message.from_user.last_name:
            user.last_name = message.from_user.last_name
        if user.username != message.from_user.username:
            user.username = message.from_user.username
        self.session.add(user)
        await self.flush()

    async def get_message_by_obj(self, message: PyrogramMessage) -> Message | None:
        # 获取消息对象
        message: Message | None = (await self.session.execute(
            select(Message).where(Message.tg_id == message.id and Message.chat_id == message.chat.id)
        )).scalars().first()
        return message

    async def delete_message(self, message: PyrogramMessage):
        # 删除消息
        message: Message | None = await self.get_message_by_obj(message)
        if message is not None:
            message.deleted = True
            logger.info(
                f'删除消息 {message.id} ({message.type.name})'
            )
            self.session.add(message)
            await self.flush()
