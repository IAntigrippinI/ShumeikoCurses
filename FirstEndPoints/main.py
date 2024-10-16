from fastapi import FastAPI, Query


hotels = [
    {"id": 1, "title": "sochi"},
    {"id": 2, "title": "dubai"},
    {"id": 3, "title": "moscow"},
]

app = FastAPI()


@app.get("/")
def func():
    return "Hello, world"


@app.get("/hotels")
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


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return "OK"


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.0", port=8080, reload=True)
