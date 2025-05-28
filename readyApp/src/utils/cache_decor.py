import json
import hashlib

from functools import wraps
from src.init import redis_manager


def acache(expire):
    """
    TODO:
    Обернуть в класс, при инициализации задавать redis, с которым действовать далее
    Понять, как выкидывать из **kwargs системные переменные, а не параметры запроса
    Понять, как определять асинзронная функция или нет
    """

    def cache(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            query_kwargs = kwargs.copy()
            del query_kwargs["db"]
            all_args = f"{func.__name__}/{query_kwargs=}"
            key = hashlib.md5(all_args.encode("utf-8")).hexdigest()
            data_from_redis = await redis_manager.get(key)

            if data_from_redis:
                data_from_redis_json = json.loads(data_from_redis)
                return data_from_redis_json

            result = await func(*args, **kwargs)
            result_dicts = [r.model_dump() for r in result]
            result_json = json.dumps(result_dicts)
            await redis_manager.set(key=key, value=result_json, expire=expire)
            return result

        return wrapper

    return cache
