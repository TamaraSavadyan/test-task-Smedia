from datetime import datetime, timedelta

from loguru import logger

from app.schemas import CustomClient
from app.config import get_config


config = get_config()

async def first_job(client: CustomClient, user_id: int):
    await client.send_message(user_id, "Добрый день!")
    logger.info(f'Succsessfully sended first message to user {user_id}')

    wake_up_at = datetime.now() + timedelta(minutes=config.SECOND_JOB_SCHEDULE_INTERVAL)
    client.scheduler.add_job(second_job, 'date', kwargs={'client': client, 'user_id': user_id}, next_run_time=wake_up_at)


async def second_job(client: CustomClient, user_id: int):
    await client.send_message(user_id, "Подготовила для вас материал")
    # подлочим евент луп, для тестового не страшно
    with open('app/fixtures/smile.png', 'rb') as f:
        await client.send_photo(user_id, f)

    logger.info(f'Succsessfully sended second message to user {user_id}')

    wake_up_at = datetime.now() + timedelta(minutes=config.THIRD_JOB_SCHEDULE_INTERVAL)
    client.scheduler.add_job(third_job, 'date', kwargs={'client': client, 'user_id': user_id}, next_run_time=wake_up_at)


async def third_job(client: CustomClient, user_id: int):
    chat_messages = await client.get_chat_history(user_id)

    async for message in chat_messages:
        if message.text == 'Хорошего дня':
            logger.info(f'Found trigger word for third message to user {user_id}, cancel sending')
            return

    await client.send_message(user_id, "Hi!")
    logger.info(f'Succsessfully sended third message to user {user_id}')
