from fastapi import APIRouter
from src.schemas.rooms import RoomsAdd, RoomsAddReq, RoomsPATCH
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        res = await RoomsRepository(session).get_by_filters(hotel_id=hotel_id)
    return res


@router.post("/{hotel_id}", description="Добавление номера")
async def add_room(hotel_id: int, data: RoomsAddReq):
    # data.hotel_id = hotel_id
    async with async_session_maker() as session:
        res = await RoomsRepository(session).add(
            RoomsAdd(
                hotel_id=hotel_id,
                title=data.title,
                description=data.description,
                price=data.price,
                quantity=data.quantity,
            )
        )
        await session.commit()
    return {"status": "OK", "message": res}


@router.put("/{hotel_id}/rooms/{room_id}", description="Изменение номера")
async def edit_room(hotel_id: int, room_id: int, data: RoomsAddReq):
    # data.hotel_id = hotel_id
    async with async_session_maker() as session:
        res = await RoomsRepository(session).edit(
            data=RoomsAdd(
                hotel_id=hotel_id,
                title=data.title,
                description=data.description,
                price=data.price,
                quantity=data.quantity,
            ),
            id=room_id,
        )
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", description="Изменение номера")
async def edit_partially_room(hotel_id: int, room_id: int, data: RoomsPATCH):
    # data.hotel_id = hotel_id
    async with async_session_maker() as session:
        res = await RoomsRepository(session).edit(data=data, id=room_id, is_patch=True)
        await session.commit()
    return {"status": "OK", "message": res}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        res = await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return "OK"
