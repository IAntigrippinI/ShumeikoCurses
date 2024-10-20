from sqlalchemy import select, insert, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(
                    location.lower()
                )  # обработка разных регистров
            )
        if title:

            query = query.filter(
                HotelsOrm.title.ilike(f"%{title}%")
            )  # ilike ищет вхождения без учета регистра (Сочи = сочи)
        query = query.limit(limit).offset(offset)
        print(query.compile(compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, title, location):
        add_hotel_stmt = insert(HotelsOrm).values(title=title, location=location)
        # print(
        #     add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})
        # )  # для вывода скомпилированного запроса SQL

        await self.session.execute(add_hotel_stmt)
        return add_hotel_stmt.compile().params
