import asyncio

import asyncpg
from pyrogram import Client, handlers, idle, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.bot import echo, get_statistics
from app.config import get_config
from app.db import UserRepository
from app.schemas import CustomClient


config = get_config()

async def bootstrap(app: Client) -> CustomClient:
    """Проделывает необходимую работу по инициализации классов нужных для работы воркера"""
    
    pool = await asyncpg.create_pool(config.PG_DSN)
    repository = UserRepository(pool)
    scheduler = AsyncIOScheduler()
    scheduler.start()

    app.db = repository
    app.scheduler = scheduler
    return app


async def main():
    app = Client("test", config.API_ID, config.API_HASH, bot_token=config.BOT_TOKEN)
    app = await bootstrap(app)
    
    app.add_handler(handlers.MessageHandler(get_statistics, filters.command('users_today')))
    app.add_handler(handlers.MessageHandler(echo))

    
    await app.start()
    await idle()
    await app.stop()

    # TODO: реализовано для бота, можно сделать для личного акка тг


if __name__ == "__main__":
    asyncio.run(main())
