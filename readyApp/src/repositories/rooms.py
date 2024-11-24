from datetime import date

from sqlalchemy import select, func
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms
from src.repositories.utils import rooms_ids_for_booking

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):

        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))

        # outerjoin = left join. for right join меняем таблицы местами (табл из селекта в join)


