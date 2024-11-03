from fastapi import APIRouter
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, RoomsPatch
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep):
    res = await db.rooms.get_filtered(hotel_id=hotel_id)
    return res


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    res = await db.rooms.get_filtered(hotel_id=hotel_id, id=room_id)
    return res


@router.post("/{hotel_id}", description="Добавление номера")
async def add_room(hotel_id: int, data: RoomsAddRequest, db: DBDep):
    room_data_add = RoomsAdd(hotel_id=hotel_id, **data.model_dump())
    res = await db.rooms.add(room_data_add)
    await db.commit()
    return {"status": "OK", "message": res}


@router.put("/{hotel_id}/rooms/{room_id}", description="Изменение номера")
async def edit_room(hotel_id: int, room_id: int, data: RoomsAddRequest, db: DBDep):
    room_data_add = RoomsAdd(hotel_id=hotel_id, **data.model_dump())

    res = await db.rooms.edit(
        data=RoomsAdd(
            hotel_id=hotel_id,
            title=data.title,
            description=data.description,
            price=data.price,
            quantity=data.quantity,
        ),
        id=room_id,
        hotel_id=hotel_id,
    )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", description="Изменение номера")
async def edit_partially_room(
    hotel_id: int, room_id: int, room_data: RoomsPatchRequest, db: DBDep
):
    _room_data = RoomsPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    # data.hotel_id = hotel_id

    await db.rooms.edit(_room_data, is_patch=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):

    res = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return "OK"
