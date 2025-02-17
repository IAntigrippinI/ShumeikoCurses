from datetime import date
from sqlalchemy import select
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_today_checkin(self):
        query = (
            select(self.model)
            .filter(BookingsOrm.date_from == date.today())
        )
        results = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(result) for result in results.scalars().all()]