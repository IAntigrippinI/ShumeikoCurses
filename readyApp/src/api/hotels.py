from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH, SchemaHotel


from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.database import engine


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


@router.get("/")
def func():
    return "Hello, world"


@router.get(
    "",
    description="Здесь описание метода",
)  # response_model=list[SchemaHotel] для валидации выходных данных
async def get_hotels(
    paginatios: PaginationDep,
    id: int | None = Query(default=None, description="идентификатор отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
    # per_page: int | None = Query(
    #     default=3, description="Кол-во объектов на странице", gt=1, lt=100
    # ),  ## gt  минимальное значение, lt максимальное значение, ge больше или равен
):

    async with async_session_maker() as session:

        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = query.limit(paginatios.per_page).offset(
            paginatios.per_page * (paginatios.page - 1)
        )

        result = await session.execute(query)
        hotels = result.scalars().all()
        # first = result.first()
        # result.one()  # выдаст ошибку, если вернулось ноль или больше одного
        # result.one_or_none()  # для проверки, вернулось ничего или один, в противном случае выдаст ошибку
    print(type(hotels), hotels)

    return hotels  # вернется адекватный json, хотя при выводе в консоль будут выводиться названия классов и адреса в памяти


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(
            add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})
        )  # для вывода скомпилированного запроса SQL
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="замена данных отеля",
    description="Здесь описание метода",
)
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotels[hotel_id - 1]["title"] = hotel_data.title
    hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичная замена данных отеля")
def edit_hotel(hotel_id: int | None, hotel_data: HotelPATCH):
    global hotels
    if hotel_data.title:
        hotels[hotel_id - 1]["title"] = hotel_data.title
    if hotel_data.name:
        hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
