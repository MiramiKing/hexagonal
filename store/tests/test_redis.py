import json
import uuid
import pytest

from app.store.adapter import ModelUser
from app.store.redis import RedisAdapter


@pytest.fixture
def adapter() -> RedisAdapter:
    return RedisAdapter


@pytest.fixture
@pytest.mark.asyncio
async def uid(adapter):
    uid = uuid.uuid4()
    await adapter.redis.set(str(uid), json.dumps(ModelUser(id=uid, first_name='Test', second_name='Test'))).to_json()
    return uid


@pytest.mark.asyncio
async def test_create_user(adapter):
    result = await adapter.create_user(ModelUser(first_name='Test', second_name='Test'))
    return isinstance(result, uuid.UUID)


@pytest.mark.asyncio
async def test_get_user(adapter, uid):
    uid = await uid
    user = await adapter.get_user(uid)
    assert user.id == uid
    assert user.first_name == 'Test'
    assert user.second_name == 'Test'


@pytest.mark.asyncio
async def test_get_user_not_exists(adapter):
    user = await adapter.get_user(uuid.uuid4())
    assert user is None


@pytest.mark.asyncio
async def test_delete_exists_user(adapter, uid):
    uid = await uid
    exists = await adapter.delete_user(uid)
    assert exists is True


@pytest.mark.asyncio
async def test_delete_non_exists_user(adapter):
    exists = await adapter.delete_user(uuid.uuid4())
    assert exists is False
