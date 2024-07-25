from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import ToDoState

SchemaType = TypeVar('SchemaType', bound=BaseModel)


class PaginationBase(BaseModel, Generic[SchemaType]):
    result: Optional[List[SchemaType]] = None
    offset: int = 0
    limit: int = 10


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDBSchema(UserSchema):
    id: int


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserListSchema(BaseModel):
    users: list[UserPublicSchema]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None


class ToDoSchema(BaseModel):
    title: str
    description: str
    state: ToDoState


class ToDoPublicSchema(ToDoSchema):
    id: int


class TodoUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    state: ToDoState | None = None
