from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.exceptions import PhoneAPIError, BinAPIError
from src.parser.BIN_cards import get_bin_cards
from src.parser.phone_region import get_region_by_phone


router = Router(name="parsers_router")

class PhoneForm(StatesGroup):
    waiting_for_number = State()

class BinForm(StatesGroup):
    waiting_for_bin = State()


def get_back_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_menu")]
        ]
    )


@router.callback_query(F.data == "phone_region")
async def ask_phone_number(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(PhoneForm.waiting_for_number)
    await callback.message.answer(
        "📞 Введите номер телефона в международном формате (например, `+79991234567`):",
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.message(PhoneForm.waiting_for_number)
async def process_phone_number(message: types.Message) -> None:

    if not message.text:
        await message.answer(
            "⚠️ Пожалуйста, отправьте номер телефона текстом:",
            reply_markup = get_back_keyboard(),
            parse_mode = "Markdown",
            )
        return

    user_phone = message.text.strip()

    try:
        user_id = message.from_user.id if message.from_user else None
        result = await get_region_by_phone(user_phone, user_id)
        await message.answer(
            f"📍 Результат проверки:\n⚡ {result}",
            reply_markup=get_back_keyboard()
        )


    except PhoneAPIError:
        await message.answer(
            "⚠️ Не удалось получить данные. Проверьте правильность "
            "номера или попробуйте позже.",
            reply_markup=get_back_keyboard()
        )


#######


@router.callback_query(F.data == "bin_cards")
async def ask_bin_number(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BinForm.waiting_for_bin)
    await callback.message.answer(
        "💳 Введите **первые 6 или 8 цифр** карты (например, `220070`):\n"
        "⚠️ _Никогда не отправляйте полный номер карты!_",
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()

@router.message(BinForm.waiting_for_bin)
async def process_bin_number(message: types.Message) -> None:

    if not message.text:
        await message.answer(
            "⚠️ Пожалуйста, отправьте первые 6–8 цифр карты текстом:",
            reply_markup = get_back_keyboard(),

            )
        return

    user_bin = message.text.strip()

    try:
        user_id = message.from_user.id if message.from_user else None
        result = await get_bin_cards(user_bin, user_id)
        await message.answer(
            f"📍 Результат проверки:\n⚡ {result}",
            reply_markup=get_back_keyboard()
        )


    except BinAPIError:
        await message.answer(
            "⚠️ Не удалось получить данные. Проверьте правильность "
            "первых 6–8 цифр карты или попробуйте позже.",
            reply_markup=get_back_keyboard()
        )