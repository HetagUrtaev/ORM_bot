from datetime import datetime

from aiogram import Router, F, types
from sqlalchemy.dialects.postgresql import insert

from src.database import async_session_maker
from src.models import UsersOrm
from src.schemas.users import UserResponse



router = Router(name="user_info_router")


@router.callback_query(F.data == 'user_info')
async def get_telegram_data(callback: types.CallbackQuery):
    is_premium_status = bool(callback.from_user.is_premium)
    current_time = datetime.now()
    u = callback.from_user

    data_user = UserResponse(
        telegram_id=u.id,
        first_name=u.first_name,
        last_name=u.last_name,
        username=u.username,
        language_code=u.language_code,
        is_premium=is_premium_status,
        is_bot=u.is_bot,
        created_at=current_time,
        last_activity_at=current_time,
    )

    info_text = (f'🆔 Ваш юзер ID: {data_user.telegram_id}\n'
            f'👤 Имя пользователя: {data_user.first_name or "Не указано"}\n'
            f'👥 Фамилия пользователя: {data_user.last_name or "Не указано"}\n'
            f'🔗 Никнейм: @{data_user.username or "Не найдено"}\n'
            f'🌐 Язык интерфейса приложения Telegram: {data_user.language_code or "Не определен"}\n'
            f'⭐️ Есть ли премиум подписка Telegram: {"Да" if data_user.is_premium else "Нет"}\n')

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


    async with async_session_maker() as session:
        stmt = insert(UsersOrm).values(**data_user.model_dump())

        stmt = stmt.on_conflict_do_update(
            index_elements=[UsersOrm.telegram_id],
            set_={'last_activity_at': stmt.excluded.last_activity_at}
        )

        await session.execute(stmt)
        await session.commit()