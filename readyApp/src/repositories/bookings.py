from datetime import date
from fastapi import HTTPException

from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_today_checkin(self):
        query = select(self.model).filter(BookingsOrm.date_from == date.today())
        results = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(result) for result in results.scalars().all()
        ]

    async def add_booking(self, booking_data: BookingAdd, hotel_id: int):
        free_rooms_ids = [
            room_id
            for room_id in (
                await self.session.execute(
                    rooms_ids_for_booking(
                        date_from=booking_data.date_from,
                        date_to=booking_data.date_to,
                        hotel_id=hotel_id,
                    )
                )
            )
            .scalars()
            .all()
        ]
        if booking_data.room_id in free_rooms_ids:
            return await self.add(data=booking_data)
        raise AllRoomsAreBookedException