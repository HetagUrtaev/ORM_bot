from datetime import datetime

from sqlalchemy import String, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(200), nullable=False)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    username: Mapped[str | None] = mapped_column(nullable=True)
    language_code: Mapped[str | None] = mapped_column(nullable=True)
    is_premium: Mapped[bool | None] = mapped_column(nullable=True)
    is_bot: Mapped[bool | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    last_activity_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
