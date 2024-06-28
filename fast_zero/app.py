from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import (
    Message,
    UserDBSchema,
    UserListSchema,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/api', status_code=HTTPStatus.OK, response_model=Message)
def root_api():
    return {'message': 'Olá Mundo!'}


@app.get('/', response_class=HTMLResponse)
def root_html():
    return """
    <html>
        <head>
            <title>Olá mundo!</title>
        </head>
        <body>
            <h1> Olá Mundo! </h1>
        </body>
    </html>
    """


@app.post(
    '/users/', response_model=UserPublicSchema, status_code=HTTPStatus.CREATED
)
def create_user(user: UserSchema):
    user_with_id = UserDBSchema(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserListSchema)
def list_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=UserPublicSchema)
def get_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return database[user_id - 1]


@app.put('/users/{user_id}', response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    user_with_id = UserDBSchema(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
