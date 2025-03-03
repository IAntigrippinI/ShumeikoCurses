

async def test_get_hotels(ac):
    responce = await ac.get(
        "/hotels",
        params={"date_from": "2024-01-12", "date_to": "2024-01-13"}
    )
    print(f"{responce.json()}")

    assert responce.status_code == 200