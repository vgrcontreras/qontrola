from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src.api.dependencies import T_Session
from src.models import User
from src.schemas.token import Token
from src.security import create_access_token, verify_password

router = APIRouter(prefix='/token', tags=['token'])


@router.post('/', status_code=HTTPStatus.OK, response_model=Token)
def login_for_access_token(
    session: T_Session, form_data: OAuth2PasswordRequestForm = Depends()
):
    user_db = session.scalar(
        select(User).where(User.email == form_data.username)
    )

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
