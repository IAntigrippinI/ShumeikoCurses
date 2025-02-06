from datetime import date

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomWithRels, Rooms
from src.repositories.utils import rooms_ids_for_booking

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):

        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
        # return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in result.scalars().unique().all()
        ]

        # outerjoin = left join. for right join меняем таблицы местами (табл из селекта в join)


    async def get_with_facilities(self, hotel_id, room_id):

        query = (
            select(self.model)
            .filter_by(id=room_id, hotel_id=hotel_id)
            .options(selectinload(self.model.facilities))
        )

        result = await self.session.execute(query)
        model = result.scalars().one()
        return RoomWithRels.model_validate(model, from_attributes=True)