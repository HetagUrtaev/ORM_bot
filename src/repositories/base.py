from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete, insert, select, update
from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper

data_user = None

class BaseRepository:
    model = None
    mapper: DataMapper = None


    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model.telegram_id)
        )
        resul = await self.session.execute(add_data_stmt)
        return resul.scalars().one()


    async def edit(self, data, exclude_unset: bool = True, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)