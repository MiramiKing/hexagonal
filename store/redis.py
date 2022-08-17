import json
import uuid
from typing import Optional
from uuid import UUID

import aioredis
from app.config.store import get_sync_db_url

from .adapter import DataBaseAdapter, ModelUser


class RedisAdapter(DataBaseAdapter):
    redis = None

    def __init__(self):
        pool = aioredis.ConnectionPool.from_url(url=get_sync_db_url(), max_connections=10)
        self.redis = aioredis.Redis(connection_pool=pool)

    async def get_user(self, uid: UUID) -> Optional[ModelUser]:
        payload = await self.redis.get(str(uid))

        if not payload:
            return None

        return ModelUser(
            id=UUID(payload.get('id')),
            first_name=payload.get('first_name'),
            second_name=payload.get('second_name'),
        )

    async def create_user(self, user: ModelUser) -> UUID:
        uid = uuid.uuid4()
        user.id = uid
        await self.redis.set(str(uid), json.dumps(user.to_json()))

    async def delete_user(self, uid: UUID) -> bool:
        if not await self.redis.exists(str(uid)):
            return False

        await self.redis.delete(str(uid))
        return True
