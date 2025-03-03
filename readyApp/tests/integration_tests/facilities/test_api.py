import pytest

# @pytest.mark.asyncio(scope="session")
async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(f'{response.json}')


# @pytest.mark.asyncio(scope="session")
async def test_create_facilities(ac):
    title = "Wi-Fi"
    response = await ac.post("/facilities", json={"title": title})

    res = response.json()
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert res['title'] == title


async def test_booking(autheticated_ac):
    response = await autheticated_ac.post("/hotels/1", json={

            "title": "Sea Room",
            "description": "Good Room",
            "price": 1200,
            "quantity": 1,
            "facilities_ids": [1]

    })
    assert response.status_code == 200
    response = await autheticated_ac.post('/bookings', json={
    'room_id': 5,
    'date_from': "2024-02-02",
    'date_to': "2024-02-03"
    })

    assert response.status_code == 200


    response = await autheticated_ac.post('/bookings', json={
    'room_id': 5,
    'date_from': "2024-02-02",
    'date_to': "2024-02-03"
    })

    assert response.status_code == 403