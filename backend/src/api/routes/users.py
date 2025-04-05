from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import CurrentUser, T_Session
from src.schemas.base import Message
from src.schemas.users import PasswordChange, UserPublic
from src.security import get_password_hash

router = APIRouter()


@router.get('/me', response_model=UserPublic)
async def get_user_info_me(current_user: CurrentUser) -> Any:
    """
    Get own account details.
    """
    return current_user


@router.patch('/me/change-password', response_model=Message)
async def update_password_me(
    session: T_Session,
    passwords: PasswordChange,
    current_user: CurrentUser,
) -> Any:
    """
    Change own password
    """
    if passwords.password != passwords.password_confirmation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Passwords dont match.'
        )

    # Set the new password with hashing
    current_user.password = get_password_hash(passwords.password)

    session.add(current_user)
    await session.commit()

    return {'message': 'Password has been changed!'}


@router.delete('/me', response_model=Message)
async def delete_user_me(
    session: T_Session, current_user: CurrentUser
) -> Message:
    """
    Delete own account.
    """
    # Soft delete - just mark as inactive
    current_user.is_active = False

    session.add(current_user)
    await session.commit()

    return Message(message='User deleted.')
