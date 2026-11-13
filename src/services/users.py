from datetime import datetime
from aiogram.types import User as TgUser

from src.schemas.users import UserResponse
from src.utils.db_manager import DBManager


class UserService:
    def __init__(self, db: DBManager) -> None:
        self.db = db

    async def upsert_from_tg(self, tg_user: TgUser) -> None:
        current_time = datetime.now()
        user_data = UserResponse(
            telegram_id=tg_user.id,
            first_name=tg_user.first_name or "Не указано",
            last_name=tg_user.last_name,
            username=tg_user.username,
            language_code=tg_user.language_code,
            is_premium=bool(tg_user.is_premium),
            is_bot=tg_user.is_bot,
            created_at=current_time,
            last_activity_at=current_time,
        )
        await self.db.users.upsert(user_data)
        await self.db.commit()
