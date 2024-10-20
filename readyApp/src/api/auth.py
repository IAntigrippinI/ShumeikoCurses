from fastapi import APIRouter, HTTPException, Response, Request

from src.schemas.users import UserRequestsAdd, UserAdd
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def registrer_user(data: UserRequestsAdd):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        async with async_session_maker() as session:
            await UsersRepository(session).add(new_user_data)
            await session.commit()

        return {"status": "OK"}
    except:
        return {"status": "error", "message": "email is busy"}


@router.post("/login")
async def login_user(data: UserRequestsAdd, responce: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session=session).get_user_with_hashed_pass(
            email=data.email
        )
        if user is None:
            raise HTTPException(status_code=401, detail="Пользователь не существует")
        if not AuthService().verify_password(
            plain_password=data.password, hashed_password=user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        responce.set_cookie("access_token", access_token)
        return {"access token": access_token}


@router.get("/only_auth")
async def only_auth(requests: Request):
    if requests.scope["headers"][-5][1].decode("utf-8").split("=")[0] == "access_token":
        access_token = requests.scope["headers"][-5][1].decode("utf-8").split("=")[0]
    else:
        access_token = None

    if access_token:
        return True
    else:
        return False
