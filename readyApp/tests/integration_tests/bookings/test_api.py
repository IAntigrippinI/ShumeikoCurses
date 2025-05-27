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


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-04-19", "2025-04-19", 200),
    (1, "2025-04-19", "2025-04-19", 200),
    (1, "2025-04-19", "2025-04-19", 200),
    (1, "2025-04-19", "2025-04-19", 200),
    (1, "2025-04-19", "2025-04-19", 200),
    (1, "2025-04-19", "2025-04-19", 403),
    (1, "2025-04-19", "2025-04-19", 403),
    (1, "2025-04-19", "2025-04-19", 403),
    (1, "2025-04-20", "2025-04-25", 200),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db,
        autheticated_ac
):

    # room_id = (await db.rooms.get_all())[0].id
    response = await autheticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
