from aiogram import Router

from src.bot.handlers.start import router as start_router
from src.bot.handlers.user_info import router as info_router
from src.bot.handlers.parser import router as parsers_router


def get_routers() -> list[Router]:
    return [
        start_router,
        info_router,
        parsers_router
    ]