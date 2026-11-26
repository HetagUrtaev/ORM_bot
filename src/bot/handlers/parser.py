from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.exceptions import PhoneAPIError
from src.parser.phone_region import get_region_by_phone


router = Router(name="parsers_router")

class PhoneForm(StatesGroup):
    waiting_for_number = State()

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
