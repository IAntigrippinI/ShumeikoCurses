from datetime import datetime

import sqlalchemy
from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
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
    try:
        room_data = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    hotel = await db.hotels.get_one(id=room_data.hotel_id)
    price = room_data.price
    try:
        schema = await db.bookings.add_booking(
            BookingAdd(
                user_id=user_id,
                price=price,
                create_at=datetime.now(),
                **booking_data.model_dump(),
            ),
            hotel_id=hotel.id,
        )
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return schema
