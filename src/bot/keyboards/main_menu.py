from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Информация о себе",
                callback_data="user_info",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
