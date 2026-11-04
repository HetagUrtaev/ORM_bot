from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.exceptions import PhoneAPIError
from src.parser.phone_region import get_region_by_phone


class TestStates(StatesGroup):
    wait_phone = State()


router = Router()


@router.message(F.text == 'Узнать регион по номеру')
async def phone_region(message: Message, state: FSMContext):
    await message.answer("Введите номер телефона:")
    await state.set_state(TestStates.wait_phone)


@router.message(TestStates.wait_phone)
async def process_phone_input(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("⚠️ Пожалуйста, отправьте номер телефона текстом:")
        return

    user_phone = message.text.strip()

    await message.answer("⏳ Проверяю номер, подождите...")

    try:
        result = await get_region_by_phone(user_phone)
        await message.answer(f"📍 Результат проверки:\n⚡ {result}")
        await state.clear()

    except PhoneAPIError:
        await message.answer("⚠️ Не удалось получить данные. Проверьте правильность номера или попробуйте позже.")
        await state.clear()