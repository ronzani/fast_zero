from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import TokenSchema
from fast_zero.security import create_access_token, get_current_user, verify_password

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=TokenSchema)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2PasswordRequestForm,
):
    user_db = session.scalar(select(User).where(User.email == form_data.username))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user_db.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=TokenSchema)
def refresh_access_token(
    user: User = Depends(get_current_user),
):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
