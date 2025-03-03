from src.connectors.redis_connector import RedisManager
from src.services.auth import AuthService


async def test_create_access_token():
    redis_manager = RedisManager(host='localhost', port=6379)
    await redis_manager.connect()
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data=data)
    assert jwt_token
    assert isinstance(jwt_token, str)
    await redis_manager.close()
