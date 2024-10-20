from sqlalchemy import func, select, insert, update, delete
from src.models.hotels import HotelsOrm
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):

        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter):

        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        # print(
        #     add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})
        # )  # для вывода скомпилированного запроса SQL

        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, filter_by: BaseModel, data: BaseModel):
        query = (
            update(self.model)
            .filter_by(**filter_by.model_dump())
            .values(**data.model_dump())
        )
        await self.session.execute(query)

    async def delete(self, filter_by: BaseModel):
        query = delete(self.model).filter_by(**filter_by.model_dump())
        await self.session.execute(query)
