from app.config.types import StoreType, store_type

from .adapter import DataBaseAdapter
from .redis import RedisAdapter
from .sql import SQLAlchemyAdapter


def get_store() -> DataBaseAdapter:
    if store_type == StoreType.REDIS:
        return RedisAdapter()
    elif store_type == StoreType.SQL:
        return SQLAlchemyAdapter
