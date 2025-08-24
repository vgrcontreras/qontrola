from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import (
    CurrentUser,
    T_Session,
    get_current_active_superuser,
)
from src.models import Client
from src.schemas.base import Message
from src.schemas.clients import (
    ClientListRequest,
    ClientRequestCreate,
    ClientRequestUpdate,
    ClientResponse,
)

# Only superusers can access client management
router = APIRouter()


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=ClientResponse,
)
async def create_client(
    session: T_Session,
    client_schema: ClientRequestCreate,
    current_user: CurrentUser,
):
    """Create a new client."""
    # Check if client with same identifier exists
    db_client = await session.scalar(
        select(Client).where(
            Client.identifier == client_schema.identifier,
        )
    )

    if db_client:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Client already exists'
        )

    client_data = client_schema.model_dump()
    db_client = Client(**client_data)

    session.add(db_client)
    await session.commit()
    await session.refresh(db_client)

    return db_client


@router.delete(
    path='/{client_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_client(
    session: T_Session,
    client_id: UUID,
):
    """Delete a client (soft delete)."""
    db_client = await session.scalar(
        select(Client).where(Client.id == client_id)
    )

    if not db_client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Client doesn't exist"
        )

    db_client.is_active = False

    session.add(db_client)
    await session.commit()

    return {'message': 'Client deleted'}


@router.patch(
    path='/{client_id}',
    status_code=HTTPStatus.OK,
    response_model=ClientResponse,
)
async def update_client(
    session: T_Session,
    client_id: UUID,
    client: ClientRequestUpdate,
    current_user: CurrentUser,
):
    """Update a client."""
    db_client = await session.scalar(
        select(Client).where(Client.id == client_id)
    )

    if not db_client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Client not found'
        )

    try:
        for key, value in client.model_dump(exclude_unset=True).items():
            setattr(db_client, key, value)

        session.add(db_client)
        await session.commit()
        await session.refresh(db_client)

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Client already exists'
        )

    return db_client


@router.get(
    path='/{client_id}',
    status_code=HTTPStatus.OK,
    response_model=ClientResponse,
)
async def get_client_by_id(
    session: T_Session,
    client_id: UUID,
    current_user: CurrentUser,
):
    """
    Get a specific client.
    """
    query = select(Client).where(Client.id == client_id)

    db_client = await session.scalar(query)

    if not db_client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Client not found'
        )

    return db_client


@router.get(
    path='/', status_code=HTTPStatus.OK, response_model=ClientListRequest
)
async def read_all_clients(
    session: T_Session,
    current_user: CurrentUser,
):
    """
    Get all clients.
    """
    query = select(Client)

    clients = await session.scalars(query)

    return {'clients': clients.all()}
