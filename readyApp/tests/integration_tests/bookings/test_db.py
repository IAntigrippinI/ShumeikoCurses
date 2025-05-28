import datetime

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.date(2025, 12, 12),
        date_to=datetime.date(2025, 12, 21),
        price=100,
        create_at=datetime.datetime(2025, 12, 12),
    )
    new_booking = await db.bookings.add(booking_data)
    print(f"{new_booking=}")

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    # assert Booking(**booking_data.model_dump(), id=1) == booking

    update_booking = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.date(2025, 12, 1),
        date_to=datetime.date(2025, 12, 21),
        price=1000,
        create_at=datetime.datetime(2025, 12, 1),
    )

    await db.bookings.edit(data=update_booking, id=booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking

    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is None
    await db.commit()
