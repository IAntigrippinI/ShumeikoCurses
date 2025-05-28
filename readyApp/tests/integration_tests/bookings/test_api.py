# async def test_booking(autheticated_ac):
#     response = await autheticated_ac.post("/hotels/1", json={
#
#             "title": "string",
#             "description": "string",
#             "price": 1200,
#             "quantity": 2,
#             "facilities_ids": [1]
#
#     })
#     assert response.status_code == 200
#     response = await autheticated_ac.post('/bookings', json={
#     'room_id': 1,
#     'date_from': "2024-02-02",
#     'date_to': "2024-02-03"
#     })
#
#     assert response.status_code == 200
import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-04-19", "2025-04-19", 200),
        (1, "2025-04-19", "2025-04-19", 200),
        (1, "2025-04-19", "2025-04-19", 200),
        (1, "2025-04-19", "2025-04-19", 200),
        (1, "2025-04-19", "2025-04-19", 200),
        (1, "2025-04-19", "2025-04-19", 403),
        (1, "2025-04-19", "2025-04-19", 403),
        (1, "2025-04-19", "2025-04-19", 403),
        (1, "2025-04-20", "2025-04-25", 200),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, db, autheticated_ac
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await autheticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)


@pytest.fixture(
    scope="module"
)  # scope=function: на каждый запуск функции прогоняется фикстура
async def delete_all_bookings(
    # db_module
):
    """
    scope=function: на каждый запуск функции прогоняется фикстура
    scope=module: запускается один раз при щапуске тестов из этого файла (модуля)/один раз для файла
    scope=session: запускается один раз на весь тест

    """
    async for (
        _db
    ) in get_db_null_pool():  # _db чтобы не было конфликтов с базовой фикстурой бд
        await _db.bookings.delete()
        await _db.commit()  # 1 способ
    # await db_module.bookings.delete() # 2 способ
    # await db_module.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, bookings_count",
    [
        (1, "2025-04-20", "2025-04-19", 200, 1),
        (1, "2025-04-20", "2025-04-19", 200, 2),
        (1, "2025-04-20", "2025-04-19", 200, 3),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    status_code,
    bookings_count,
    delete_all_bookings,
    autheticated_ac,
):
    response = await autheticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code

    response_bookings = await autheticated_ac.get("bookings/me")
    with open("test.txt", "a") as f:
        f.write(f"\n\n{response_bookings.json()}")
    assert len(response_bookings.json()) == bookings_count
