from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select, func

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH, SchemaHotel


from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.database import engine
from src.repositories.hotels import HotelsRepository


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


@router.get(
    "",
    description="Здесь описание метода",
)  # response_model=list[SchemaHotel] для валидации выходных данных
async def get_hotels(
    paginatios: PaginationDep,
    location: str | None = Query(default=None, description="Локация отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
    # per_page: int | None = Query(
    #     default=3, description="Кол-во объектов на странице", gt=1, lt=100
    # ),  ## gt  минимальное значение, lt максимальное значение, ge больше или равен
):

    async with async_session_maker() as session:

        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=paginatios.per_page,
            offset=paginatios.per_page * (paginatios.page - 1),
        )

        # first = result.first()
        # result.one()  # выдаст ошибку, если вернулось ноль или больше одного
        # result.one_or_none()  # для проверки, вернулось ничего или один, в противном случае выдаст ошибку


# return hotels  # вернется адекватный json, хотя при выводе в консоль будут выводиться названия классов и адреса в памяти


@router.post(
    "", summary="добавление отеля", description="<h1>Здесь описание метода</h1>"
)
async def create_hotel(
    hotel_data: Hotel = Body(
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
    )
):

    async with async_session_maker() as session:

        hotel = await HotelsRepository(session).add(hotel_data)
        print(hotel)
        await session.commit()
        return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="замена данных отеля",
    description="Здесь описание метода",
)
async def edit_hotel(hotel_data: Hotel, hotel_new_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, hotel_new_data)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичная замена данных отеля")
async def edit_hotel(hotel_id: int | None, hotel_data: HotelPATCH):

    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(hotel_data)
        await session.commit()
    return {"status": "OK"}
