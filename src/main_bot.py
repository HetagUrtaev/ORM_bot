import asyncio


from aiogram import Bot, Dispatcher

from src.bot.handlers import get_routers
from src.bot.middlewares.db import DBMiddleware
from src.config import settings
from src.init import redis_manager
import logging
logging.basicConfig(level=logging.INFO)

async def main() -> None:
    bot = Bot(token=settings.TOKEN)

    await redis_manager.connect()
    print("✅ Redis подключен")

    dp = Dispatcher()
    dp.update.middleware(DBMiddleware())
    dp.include_routers(*get_routers())

    print("🚀 Запуск бота...")
    try:
        await dp.start_polling(bot)
    finally:
        await redis_manager.disconnect()
        await bot.session.close()
        print("🛑 Бот и Redis остановлены")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nПрограмма принудительно завершена.')