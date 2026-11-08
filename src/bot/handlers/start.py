from aiogram import Router
from aiogram import types
from aiogram.filters import Command


router = Router(name="start")


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Информация о себе 👤")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
        input_field_placeholder="Выбери интересующий раздел?")
    await message.answer("Выбери интересующий раздел?", reply_markup=keyboard)


