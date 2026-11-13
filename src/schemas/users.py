from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    is_premium: bool | None
    is_bot: bool | None


class UserResponse(UserCreate):
    created_at: datetime
    last_activity_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserPatch(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    last_activity_at: datetime | None = None