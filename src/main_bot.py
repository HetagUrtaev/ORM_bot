import asyncio

from aiogram import Bot, Dispatcher

from src.bot.handlers import get_routers
from src.config import settings


async def main() -> None:

    bot = Bot(token=settings.TOKEN)

    dp = Dispatcher()

    dp.include_routers(*get_routers())

    print("🚀 Запуск бота...")
    try:
        await dp.start_polling(bot)
    finally:
        print("🛑 Бот остановлен")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('\nПрограмма принудительно завершена.')