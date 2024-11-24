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

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotel_ids_to_get))
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
        query = query.limit(pagination.per_page).offset(
            (pagination.page - 1) * pagination.per_page
        )
        result = await self.session.execute(query)

        return [
            Hotel.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]
