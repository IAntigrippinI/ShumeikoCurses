import typing

import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self) -> None:
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def set(self, key: str, value: str, expire: int = None) -> None:
        if expire:
            await self.redis.set(name=key, value=value, ex=expire)
        else:
            await self.redis.set(name=key, value=value)

    async def get(self, key: str) -> typing.Any | None:
        return await self.redis.get(name=key)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def close(self) -> None:
        if self.redis:
            await self.redis.aclose()
