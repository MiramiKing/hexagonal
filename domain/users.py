from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from fastapi import status

from app.messages import (
    CreateUserMessage, CreateUserResultMessage, DeleteUserMessage,
    DeleteUserResultMessage, GetUserMessage, GetUserResultMessage,
)

from app.store.adapter import DataBaseAdapter


@dataclass
class InternalException(Exception):
    errors: dict
    status: int = 400


class IUsersApp(metaclass=ABCMeta)

    @abstractmethod
    async def create_user(self, msg: CreateUserMessage) -> CreateUserResultMessage:
        pass

    @abstractmethod
    async def delete_user(self, msg: DeleteUserMessage) -> DeleteUserResultMessage:
        pass

    @abstractmethod
    async def get_user(self, msg: GetUserMessage) -> GetUserResultMessage:
        pass


class UserApp(IUsersApp):
    adapter: DataBaseAdapter

    def __init__(self, adapter: DataBaseAdapter):
        self.adapter = adapter

    async def create_user(self, msg: CreateUserMessage) -> CreateUserResultMessage:
        uid = self.adapter.create_user(msg.to_user())
        return CreateUserResultMessage(id=uid)

    async def delete_user(self, msg: DeleteUserMessage) -> DeleteUserResultMessage:
        exists = await self.adapter.delete_user(msg.id)
        return DeleteUserResultMessage(exists=exists)

    async def get_user(self, msg: GetUserMessage) -> GetUserResultMessage:
        user = await self.adapter.get_user(msg.id)

        if not user:
            raise InternalException({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        return GetUserResultMessage(id=user.id, first_name=user.first_name, second_name=user.second_name)
