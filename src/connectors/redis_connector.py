import logging

from redis.asyncio import Redis


class RedisManager:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.host = host
        self.port = port
        self.redis: Redis | None = None

    async def connect(self) -> None:

        logging.info(f"Начинаю подключение к Redis host={self.host}, port={self.port}")
        self.redis = Redis(host=self.host, port=self.port, decode_responses=True)
        await self.redis.ping()
        logging.info(f"Успешное подключение к Redis host={self.host}, port={self.port}")


    async def set(self, key: str, value: str, expire: int | None = None) -> bool:

        if expire:
            return await self.redis.set(key, value, ex=expire)
        else:
            return await self.redis.set(key, value)

    async def get(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def delete(self, key: str) -> int:
        return await self.redis.delete(key)

    async def disconnect(self) -> None:
        if self.redis:
            await self.redis.close()
            logging.info("Соединение с Redis успешно закрыто.")