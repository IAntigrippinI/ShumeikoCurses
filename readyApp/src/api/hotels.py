from fastapi import Query, Body, APIRouter

from src.schemas.hotels import Hotel, HotelPATCH, SchemaHotel
from src.api.dependencies import PaginationDep

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


@router.get("", description="Здесь описание метода", response_model=list[SchemaHotel])
def get_hotels(
    paginatios: PaginationDep,
    id: int | None = Query(default=None, description="идентификатор отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
    # page: int | None = Query(default=1, description="Страница", gt=1),
    # per_page: int | None = Query(
    #     default=3, description="Кол-во объектов на странице", gt=1, lt=100
    # ),  ## gt  минимальное значение, lt максимальное значение, ge больше или равен
):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[
        (paginatios.page - 1)
        * paginatios.per_page : paginatios.page
        * paginatios.per_page
    ]


@router.post(
    "", summary="добавление отеля", description="<h1>Здесь описание метода</h1>"
)
def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Отель Сочи Звезда", "name": "Сочи Море"},
            },
            "2": {
                "summary": "Владивосток",
                "value": {"title": "Отель СПА ВДК", "name": "Ночь Владивостока"},
            },
        }
    )
):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1, "title": hotel_data.title, "name": hotel_data.name}
    )
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
