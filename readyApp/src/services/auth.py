import jwt

from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.config import settings


class AuthService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError as e:
            raise HTTPException(status_code=401, detail="Невверный токен")
