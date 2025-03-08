from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.settings import settings

T_Session = Annotated[Session, Depends(get_session)]

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(clean_password: str, hashed_password: str):
    return pwd_context.verify(clean_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_current_user(session: T_Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user_db = session.scalar(select(User).where(User.email == subject_email))

    if not user_db:
        raise credentials_exception

    return user_db
