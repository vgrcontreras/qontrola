from http import HTTPStatus
from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.core.settings import settings
from src.models import User

T_Session = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


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
