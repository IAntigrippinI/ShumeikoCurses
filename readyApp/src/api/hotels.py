from datetime import date

from fastapi import Query, Body, APIRouter
from fastapi_cache.decorator import cache

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH, SchemaHotel, HotelAdd


from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker
from src.database import engine
from src.repositories.hotels import HotelsRepository
from src.utils.cache_decor import acache


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "sochi", "name": "sss"},
    {"id": 2, "title": "dubai", "name": "ddd"},
    {"id": 3, "title": "moscow", "name": "mmm"},
    {"id": 4, "title": "moscow", "name": "mmm"},
    {"id": 5, "title": "moscow", "name": "mmm"},
    {"id": 6, "title": "moscow", "name": "mmm"},
    {"id": 7, "title": "moscow", "name": "mmm"},
]


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.get(
    "",
    description="Здесь описание метода",
)  # response_model=list[SchemaHotel] для валидации выходных данных
@acache(expire=30)
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

    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=paginatios.per_page,
    #     offset=paginatios.per_page * (paginatios.page - 1),
    # )

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        pagination=pagination,
    )

    # first = result.first()
    # result.one()  # выдаст ошибку, если вернулось ноль или больше одного
    # result.one_or_none()  # для проверки, вернулось ничего или один, в противном случае выдаст ошибку


# return hotels  # вернется адекватный json, хотя при выводе в консоль будут выводиться названия классов и адреса в памяти


@router.post(
    "", summary="добавление отеля", description="<h1>Здесь описание метода</h1>"
)
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
    async with async_session_maker() as session:
        await db.hotels.edit(data=hotel_data, id=hotel_id)
        await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичная замена данных отеля")
async def edit_hotel(hotel_id: int | None, hotel_data: HotelPATCH, db: DBDep):

    await db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
