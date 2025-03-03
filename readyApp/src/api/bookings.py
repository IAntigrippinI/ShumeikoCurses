from datetime import datetime

from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    result = await db.bookings.get_filtered(user_id=user_id)
    return result


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    room_data = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room_data:
        price = room_data.price
    else:

        raise HTTPException(status_code=422, detail="Неверный id номера")
    schema = await db.bookings.add_booking(
        BookingAdd(
            user_id=user_id,
            price=price,
            create_at=datetime.now(),
            **booking_data.model_dump()
        ),
        hotel_id=room_data.hotel_id
    )
    await db.commit()
    return schema
