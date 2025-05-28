from src.schemas.hotels import HotelAdd



async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Hotel 5 s", location="Анапа")
    new_hotel_data = await db.hotels.add(hotel_data)
    print(f"{new_hotel_data=}")
    await db.commit()


async def test_add_hotel2(db):
    hotel_data = HotelAdd(title="Hotel 5-8 s", location="Анапа")
    new_hotel_data = await db.hotels.add(hotel_data)
    print(f"{new_hotel_data=}")
    await db.commit()
