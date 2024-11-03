from fastapi import APIRouter, HTTPException, Response, Request

from src.schemas.users import UserRequestsAdd, UserAdd
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def registrer_user(data: UserRequestsAdd, db: DBDep):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:

        await db.users.add(new_user_data)
        await db.commit()

        return {"status": "OK"}
    except:
        return {"status": "error", "message": "email is busy"}


@router.post("/login")
async def login_user(data: UserRequestsAdd, responce: Response, db: DBDep):

    user = await db.users.get_user_with_hashed_pass(email=data.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не существует")
    if not AuthService().verify_password(
        plain_password=data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    responce.set_cookie("access_token", access_token)
    return {"access token": access_token}


@router.get("/me")
async def get_me(requests: Request, user_id: UserIdDep, db: DBDep):

    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(responce: Response):
    responce.delete_cookie("access_token")
    return "OK"
