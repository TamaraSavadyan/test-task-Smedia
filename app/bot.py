from datetime import datetime, timedelta

from pyrogram import types

from app.schemas import CustomClient
from app.schedulers import first_job
from app.config import get_config


config = get_config()

async def echo(client: CustomClient, message: types.Message):
    # 1. Делаем запрос в базу, смотрим есть ли там клиент
    user = await client.db.get_user_by_id(message.from_user.id)

    # 2. если клиент уже есть в бд ничего не делаем
    if user is not None:
        return

    # 3. Сохраняем юзера в бд
    await client.db.put_user_in_db(message.from_user.id)

    # 3. Запускаем воронки
    wake_up_at = datetime.now() + timedelta(minutes=config.FIRST_JOB_SCHEDULE_INTERVAL)
    client.scheduler.add_job(first_job, 'date', kwargs={'client': client, 'user_id': message.from_user.id}, next_run_time=wake_up_at)


async def get_statistics(client: CustomClient, message: types.Message):
    total_users = await client.db.get_user_statistics()
    await client.send_message(message.from_user.id, f"Кол-во пользователей за сегодня - {total_users}")
