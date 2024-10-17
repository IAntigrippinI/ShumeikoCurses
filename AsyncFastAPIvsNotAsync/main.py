from fastapi import FastAPI, Query, Body
import time
import asyncio
import threading

hotels = [
    {"id": 1, "title": "sochi"},
    {"id": 2, "title": "dubai"},
    {"id": 3, "title": "moscow"},
]

app = FastAPI()


@app.get("/")
def func():
    return "Hello, world"


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time():.2f}")


@app.get("/hotels", description="Здесь описание метода")
def get_hotels(
    id: int | None = Query(default=None, description="идентификатор отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post(
    "/hotels", summary="добавление отеля", description="<h1>Здесь описание метода</h1>"
)
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "data": title})
    return {"status": "OK"}


@app.put(
    "/hotels/{hotel_id}",
    summary="замена данных отеля",
    description="Здесь описание метода",
)
def edit_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    hotels[hotel_id - 1]["title"] = title
    hotels[hotel_id - 1]["name"] = str
    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}", summary="Частичная замена данных отеля")
def edit_hotel(
    hotel_id: int | None, title: str | None = Body(None), name: str | None = Body(None)
):
    global hotels
    if title:
        hotels[hotel_id - 1]["title"] = title
    if name:
        hotels[hotel_id - 1]["name"] = name
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.0", port=8080, workers=5)
