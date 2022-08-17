from abc import ABCMeta, abstractmethod
from typing import Optional

from app.domain.users import IUsersApp
from app.messages import (
    CreateUserMessage, CreateUserResultMessage, DeleteUserMessage,
    DeleteUserResultMessage, GetUserMessage, GetUserResultMessage,
)


class IMessageBus(metaclass=ABCMeta):

    @abstractmethod
    async def handle(self, message: Optional[CreateUserMessage, DeleteUserMessage, GetUserMessage]) -> Optional[
        CreateUserResultMessage, GetUserResultMessage, DeleteUserResultMessage]:
        pass


class MessageBus(IMessageBus):
    app: IUsersApp = None

    def __init__(self, app: IUsersApp):
        self.app = app

    async def handle(self, msg: Optional[CreateUserMessage, DeleteUserMessage, GetUserMessage]) -> Optional[CreateUserResultMessage, GetUserResultMessage, DeleteUserResultMessage]:
        msg.validate()

        if msg == CreateUserMessage:
            return await self.app.create_user(msg)
        elif msg == DeleteUserMessage:
            return await self.app.delete_user(msg)
        elif msg == GetUserMessage:
            return await self.app.get_user(msg)
