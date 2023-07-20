from pydantic_settings import BaseSettings
from typing import Optional as Opt


class Settings(BaseSettings):
    telegram_api_id: int
    telegram_api_hash: str

    api_host: Opt[str] = 'localhost'
    api_port: Opt[int] = 8080

    auth: Opt[str] = 'none'
    # none, password, webauthn (todo)

    postgresql_host: Opt[str] = 'localhost'
    postgresql_port: Opt[int] = 5432
    postgresql_user: Opt[str] = 'zhubiapp'
    postgresql_password: Opt[str] = ''
    postgresql_database: Opt[str] = 'zhubiapp'

    loglevel: Opt[str] = 'INFO'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'zhubiapp_'
        case_sensitive = False


settings = Settings()

app_version: str = '0.0.1'
