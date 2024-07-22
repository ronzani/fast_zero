from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import ToDoState


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


class TodoSchema(BaseModel):
    title: str
    description: str
    state: ToDoState


class TodoPublicSchema(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublicSchema]
