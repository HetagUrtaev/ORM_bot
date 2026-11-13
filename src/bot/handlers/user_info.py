from datetime import datetime
from aiogram import Router, F, types

from src.services.users import UserService
from src.utils.db_manager import DBManager

router = Router(name="user_info_router")


@router.callback_query(F.data == 'user_info')
async def get_telegram_data(callback: types.CallbackQuery, db: DBManager) -> None:
    user = callback.from_user



    info_text = (f'🆔 Ваш юзер ID: {user.id}\n'
            f'👤 Имя пользователя: {user.first_name or "Не указано"}\n'
            f'👥 Фамилия пользователя: {user.last_name or "Не указано"}\n'
            f'🔗 Никнейм: @{user.username or "Не найдено"}\n'
            f'🌐 Язык интерфейса приложения Telegram: {user.language_code or "Не определен"}\n'
            f'⭐️ Есть ли премиум подписка Telegram: {"Да" if user.is_premium else "Нет"}\n')

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="⬅️ Назад в меню",
                    callback_data="back_to_menu",
                )
            ]
        ]
    )

    await callback.message.answer(info_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
    await UserService(db).upsert_from_tg(user)

