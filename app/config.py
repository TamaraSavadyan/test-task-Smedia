from functools import lru_cache
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Bot
    API_ID: str
    API_HASH: str
    BOT_TOKEN: str

    # Database
    PG_DSN: str

    # Job config
    FIRST_JOB_SCHEDULE_INTERVAL: int = 10 # в минутах
    SECOND_JOB_SCHEDULE_INTERVAL: int = 90 # в минутах
    THIRD_JOB_SCHEDULE_INTERVAL: int = 120 # в минутах


@lru_cache
def get_config():
    return Config()
