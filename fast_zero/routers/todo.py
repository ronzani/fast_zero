from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import ToDo, ToDoState, User
from fast_zero.schemas import (
    PaginationBase,
    ToDoPublicSchema,
    ToDoSchema,
)
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todo', tags=['todo'])

Session = Annotated[Session, Depends(get_session)]
User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=ToDoPublicSchema, status_code=HTTPStatus.CREATED)
def create_todo(
    todo: ToDoSchema,
    user: User,
    session: Session,
):
    db_todo = ToDo(
        user_id=user.id,
        title=todo.title,
        description=todo.description,
        state=todo.state,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=PaginationBase[ToDoPublicSchema])
def list_to_dos(  # noqa: PLR0913 PLR0917
    session: Session,
    user: User,
    title: str = None,
    description: str = None,
    state: ToDoState | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = select(ToDo).where(ToDo.user_id == user.id)

    if title:
        query = query.filter(ToDo.title.icontains(title))

    if description:
        query = query.filter(ToDo.description.icontains(description))

    if state:
        query = query.filter(ToDo.state == state)

    to_dos = session.scalars(query.offset(offset).limit(limit))

    return {'result': to_dos, 'offset': offset, 'limit': limit}
