from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src.api.dependencies import CurrentUser, T_Session
from src.models import User
from src.schemas.token import Token
from src.security import create_access_token, verify_password

router = APIRouter()


@router.post('/', status_code=HTTPStatus.OK, response_model=Token)
async def login_for_access_token(
    session: T_Session,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Find user
    user_db = await session.scalar(
        select(User).where(
            (User.email == form_data.username) & (User.is_active == True)  # noqa: E712
        )
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

    # Create access token
    access_token = create_access_token(
        data={
            'sub': user_db.email,
            'is_superuser': user_db.is_superuser,
        }
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(
        data={
            'sub': user.email,
            'is_superuser': user.is_superuser,
        }
    )

    return {'access_token': new_access_token, 'token_type': 'bearer'}
