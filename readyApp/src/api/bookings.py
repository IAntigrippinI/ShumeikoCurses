from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    room_data = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room_data:
        price = room_data.price
    else:

        raise HTTPException(status_code=422, detail="Неверный id номера")
    schema = await db.bookings.add(
        BookingAdd(
            room_id=booking_data.room_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            user_id=user_id,
            price=price * (booking_data.date_to - booking_data.date_from).days,
        )
    )
    await db.commit()
    return schema
