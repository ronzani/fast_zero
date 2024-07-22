from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User, ToDo
from fast_zero.schemas import TodoPublicSchema, TodoSchema
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todo', tags=['todo'])

Session = Annotated[Session, Depends(get_session)]
User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublicSchema, status_code=HTTPStatus.CREATED)
def create_todo(
    todo: TodoSchema,
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
