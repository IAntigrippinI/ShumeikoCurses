import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app


@pytest.mark.parametrize("email, password, status", [
    ("test@mail.ru", "123", 200),
    ("test@mail.ru", "1234", 400),
    ("python@mail.ru", "123", 200),
    ("python", "123", 422),
    ("python", "", 422),
])
async def test_user_api(
    email, password, status,
):
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test1234") as ac:
            #register
            data=dict(email=email, password=password)
            response = await ac.post("/auth/register", json=data)

            assert response.status_code == status

            if response.status_code != 200:
                return
            #login
            response = await ac.post("/auth/login", json=data)

            assert response.status_code == status
            assert response.cookies.get("access_token", None)

            #me
            response = await ac.get("/auth/me")

            assert response.status_code == status
            assert response.json().get("email", None)

            #logout
            response = await ac.post("/auth/logout")

            assert response.status_code == status
            assert response.cookies.get("access_token", None) is None