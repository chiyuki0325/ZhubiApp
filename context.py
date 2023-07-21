# 上下文变量

from pyrogram import Client
from database.database import Database
from datetime import datetime

client: Client | None = None
db: Database | None = None
token: str | None = None
token_last_used: datetime | None = None
