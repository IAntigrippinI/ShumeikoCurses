from datetime import date

from sqlalchemy import select, insert, func


from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.schemas.hotels import Hotel
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

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
        return [
            Hotel.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location: str,
        title: str,
        pagination,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotel_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.hotel_id.in_(rooms_ids_to_get))
        )
        if location:
            hotel_ids_to_get = hotel_ids_to_get.filter(
                HotelsOrm.location.ilike(f"%{location}%")
            )
        if title:
            hotel_ids_to_get = hotel_ids_to_get.filter(
                HotelsOrm.title.ilike(f"%{title}%")
            )
        hotel_ids_to_get = hotel_ids_to_get.limit(pagination.per_page).offset(
            (pagination.page - 1) * pagination.per_page
        )
        return await self.get_filtered(HotelsOrm.id.in_(hotel_ids_to_get))
