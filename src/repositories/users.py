from sqlalchemy.dialects.postgresql import insert

from src.models import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserResponse


class UsersRepository(BaseRepository):
    model = UsersOrm
    schemas = UserResponse

    async def upsert(self, data: UserResponse) -> None:
        stmt = insert(self.model).values(**data.model_dump())
        stmt = stmt.on_conflict_do_update(
            index_elements=[self.model.telegram_id],
            set_={"last_activity_at": stmt.excluded.last_activity_at},
        )
        await self.session.execute(stmt)