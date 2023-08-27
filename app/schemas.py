from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client

from app.db import UserRepository


class CustomClient(Client): # нужно для тайпинга, возможно можно реализовать более элегантно
    db: UserRepository
    scheduler: AsyncIOScheduler
