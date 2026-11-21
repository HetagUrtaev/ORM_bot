from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Информация о себе",
                callback_data="user_info",
            ),
            InlineKeyboardButton(
                text="📱 Узнать регион по номеру",
                callback_data="phone_region",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
