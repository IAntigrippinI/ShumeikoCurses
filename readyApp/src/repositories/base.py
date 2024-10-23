from sqlalchemy import func, select, insert, update, delete
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):

        query = select(self.model)
        result = await self.session.execute(query)

    async def get_by_filters(self, **filter):
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)

        model = result.scalars().all()
        print(query.compile(compile_kwargs={"literal_binds": True}))
        if model is None:
            return None
        else:
            return model
            return [
                self.schema.model_validate(model, from_attributes=True)
                for model in result.scalars().all()
            ]

    async def get_one_or_none(self, **filter):

        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        if model is None:
            return None
        else:

            return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        # print(
        #     add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})
        # )  # для вывода скомпилированного запроса SQL

        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

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

    # async def get_one_or_none(self, id: int):
    #     query = select(self.model).filter_by(id=id)
    #     result = await self.session.execute(query)
    #     return result.scalars().one_or_none()

    # async def delete(self, filter_by: BaseModel): # вариант с фильтрацией через многие признаки
    #     query = delete(self.model).filter_by(**filter_by.model_dump())
    #     await self.session.execute(query)
