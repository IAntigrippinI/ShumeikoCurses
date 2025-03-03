async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200

    print(f'{response.json}')


async def test_create_facilities(ac):
    response = await ac.post("/facilities", data='{"title": "string"}')


    assert response.status_code == 200
