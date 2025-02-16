from sqlalchemy import func, select, insert, update, delete, or_
from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(data=model)
            for model in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter):

        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        if model is None:
            return None
        else:
            return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        # print(
        #     add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})
        # )  # для вывода скомпилированного запроса SQL

        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
    
    
    async def add_bulk(self, data: list[BaseModel]): # bulk - много
        add_data_stmt = (
            insert(self.model).values([item.model_dump() for item in data]).returning(self.model)
        )
        await self.session.execute(add_data_stmt)
      

    async def edit(self, data: BaseModel, is_patch: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=is_patch))
        )
        await self.session.execute(update_stmt)


    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)


    async def delete_bulk(self, *filter,**filter_by):
        delete_stmt = delete(self.model).filter(*filter).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
