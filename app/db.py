from asyncpg import Pool, Connection


class UserRepository:
    def __init__(self, db: Pool):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> int | None:
        async with self.db.acquire() as session:
            session: Connection
            result = await session.fetchrow("SELECT id FROM test.telegram_users WHERE id = $1", user_id)
            return result

    async def put_user_in_db(self, user_id: int):
        async with self.db.acquire() as session:
            session: Connection
            result = await session.execute('INSERT INTO test.telegram_users ("id") VALUES ($1)', user_id)
            return result

    async def get_user_statistics(self):
        async with self.db.acquire() as session:
            session: Connection
            result = await session.fetchval("SELECT count(1) FROM test.telegram_users WHERE created_at > now() + interval '1 days'")
            return result
