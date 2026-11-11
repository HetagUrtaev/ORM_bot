from aiogram import Router, F, types
from aiogram.filters import Command

from src.bot.keyboards.main_menu import get_main_menu_keyboard

router = Router(name="start")


async def send_main_menu(event: types.Message | types.CallbackQuery) -> None:
    text = "👋 Добро пожаловать!"
    keyboard = get_main_menu_keyboard()

    if isinstance(event, types.CallbackQuery):
        await event.message.answer(text, reply_markup=keyboard)
        await event.answer()
    else:
        await event.answer(text, reply_markup=keyboard)



@router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    await send_main_menu(message)



@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: types.CallbackQuery) -> None:
    await send_main_menu(callback)





