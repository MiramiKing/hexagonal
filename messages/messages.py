from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.store.adapter import ModelUser


@dataclass
class ValidateException(Exception):
    errors: dict

    def __str__(self):
        return self.errors['message']


class BaseResponse(metaclass=ABCMeta):

    @abstractmethod
    def to_json(self) -> dict:
        pass


class BaseRequest(metaclass=ABCMeta):

    @abstractmethod
    def validate(self):
        pass


@dataclass
class CreateUserMessage(BaseRequest):
    first_name: str
    second_name: str

    def to_user(self) -> ModelUser:
        return ModelUser(first_name=self.first_name, second_name=self.second_name)

    def validate(self):
        if self.first_name is None:
            raise ValidateException(errors={'message': '"first_name" not defined'})
        if self.second_name is None:
            raise ValidateException(errors={'message': '"second_name" not defined'})


@dataclass
class CreateUserResultMessage(BaseResponse):
    id: UUID

    def to_json(self) -> dict:
        return {'id': self.id}

    def __str__(self):
        return str(self.id)


@dataclass
class GetUserMessage(BaseRequest):
    id: UUID

    def validate(self):
        if self.id is None:
            raise ValidateException(errors={'message': '"id" not defined'})


@dataclass
class GetUserResultMessage(BaseResponse):
    id: UUID
    first_name: str
    second_name: str

    def to_json(self):
        return {'id': self.id, 'first_name': self.first_name, 'second_name': self.second_name}

    def __str__(self):
        return f'ID: {self.id}, First name: {self.first_name}, Second name: {self.second_name}'


@dataclass
class DeleteUserMessage(BaseRequest):
    id: UUID

    def validate(self):
        if self.id is None:
            raise ValidateException(errors={'message': '"id" not defined'})


@dataclass
class DeleteUserResultMessage(BaseResponse):
    exists: bool

    def to_json(self) -> dict:
        return {'exists': self.exists}

    def __str__(self):
        if self.exists:
            return 'deleted'
        return 'not found'