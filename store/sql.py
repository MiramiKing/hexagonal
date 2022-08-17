import uuid
from typing import Optional

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.store import get_async_db_url
from .adapter import DataBaseAdapter, ModelUser

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column('first_name', String(50), nullable=False)
    second_name = Column('second_name', String(50), nullable=False)

    def __repr__(self):
        return f'User(id={self.id!r}, first_name={self.first_name!r}, second_name={self.second_name!r})'


class SQLAlchemyAdapter(DataBaseAdapter):
    engine = None
    Session = None

    def __init__(self):
        self.engine = create_async_engine(get_async_db_url(), echo=True, future=True)
        self.Session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def get_user(self, uid: UUID) -> Optional[ModelUser]:
        async with self.Session() as session:
            user = await session.get(User, uid)

            if user is None:
                return None

            return ModelUser(
                id=user.id,
                first_name=user.first_name,
                second_name=user.second_name
            )

    async def create_user(self, user: ModelUser) -> UUID:
        async with self.Session() as session:
            orm_user = User(
                id=uuid.uuid4(),
                first_name=user.first_name,
                second_name=user.second_name
            )
            session.add(orm_user)
            await session.commit()

            return orm_user.id

    async def delete_user(self, uid: UUID) -> bool:
        async with self.Session() as session:
            user = await session.get(User, uid)

            if user is None:
                return False

            await session.delete(user)
            await session.commit()
            return True
