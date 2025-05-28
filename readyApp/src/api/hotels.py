from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException
from src.schemas.hotels import HotelPATCH, HotelAdd


from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

@router.get(
    "",
    description="Здесь описание метода",
)  # response_model=list[SchemaHotel] для валидации выходных данных
# @cache(expire=30)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(default=None, description="Локация отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
    date_from: date = Query(example="2024-11-17"),
    date_to: date = Query(example="2024-11-18"),
    # per_page: int | None = Query(
    #     default=3, description="Кол-во объектов на странице", gt=1, lt=100
    # ),  ## gt  минимальное значение, lt максимальное значение, ge больше или равен
):

    if date_to < date_from:
        raise HTTPException(status_code=400, detail="Дата выезда позже даты заезда")
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        pagination=pagination,
    )


@router.post("", summary="добавление отеля", description="<h1>Здесь описание метода</h1>")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи Звезда",
                    "location": "Сочи, ул. Портовая, 5",
                },
            },
            "2": {
                "summary": "Владивосток",
                "value": {
                    "title": "Отель СПА",
                    "location": "Владивосток, ул. 1, 1",
                },
            },
        }
    ),
):
    hotel = await db.hotels.add(hotel_data)
    print(hotel)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="замена данных отеля",
    description="Здесь описание метода",
)
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичная замена данных отеля")
async def part_edit_hotel(hotel_id: int | None, hotel_data: HotelPATCH, db: DBDep):
    await db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
