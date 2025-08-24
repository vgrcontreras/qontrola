from http import HTTPStatus
from uuid import UUID

from src.schemas.clients import ClientResponse


def test_create_client(api_client, superuser_token) -> None:
    response = api_client.post(
        url='/clients',
        json={
            'name': 'client1',
            'client_type': 'velas',
            'type_identifier': 'cnpj',
            'identifier': '12345678901234',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['name'] == 'client1'
    assert data['client_type'] == 'velas'
    assert data['type_identifier'] == 'cnpj'
    assert data['identifier'] == '12345678901234'
    # Verify UUID format
    assert UUID(data['id']) is not None


def test_create_client_already_exists(
    api_client, db_client, superuser_token
) -> None:
    response = api_client.post(
        url='/clients',
        json={
            'name': 'client1',
            'client_type': 'velas',
            'type_identifier': 'cnpj',
            'identifier': '12345678901234',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Client already exists'}


def test_delete_client(api_client, db_client, superuser_token) -> None:
    response = api_client.delete(
        url=f'/clients/{db_client.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Client deleted'}


def test_delete_client_not_found(api_client, superuser_token) -> None:
    response = api_client.delete(
        url='/clients/123e4567-e89b-12d3-a456-426614174000',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Client doesn't exist"}


def test_update_client_not_found(api_client, superuser_token) -> None:
    response = api_client.patch(
        url='/clients/123e4567-e89b-12d3-a456-426614174000',
        json={'name': 'test_update_name'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}


def test_update_client(api_client, db_client, superuser_token) -> None:
    response = api_client.patch(
        url=f'/clients/{db_client.id}',
        json={'name': 'test_updated_name'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['name'] == 'test_updated_name'
    assert data['client_type'] == 'test'
    assert data['type_identifier'] == 'cnpj'
    assert data['identifier'] == '12345678901234'
    assert UUID(data['id']) == db_client.id


def test_update_client_integrity_error(
    api_client, db_client, superuser_token
) -> None:
    # creating a new client
    api_client.post(
        url='/clients',
        json={
            'name': 'client1',
            'client_type': 'velas',
            'type_identifier': 'cnpj',
            'identifier': '12345678901235',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    response = api_client.patch(
        url=f'/clients/{db_client.id}',
        json={'identifier': '12345678901235'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Client already exists'}


def test_get_all_clients(
    session, api_client, db_client, superuser_token
) -> None:
    client_schema = ClientResponse.model_validate(db_client).model_dump()
    response = api_client.get(
        url='/clients',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    # Get the clients list and verify it contains our client data
    response_data = response.json()
    assert 'clients' in response_data
    assert len(response_data['clients']) == 1

    # Check important fields individually rather than comparing entire objects
    response_client = response_data['clients'][0]
    assert response_client['name'] == client_schema['name']
    assert response_client['client_type'] == client_schema['client_type']
    assert response_client['identifier'] == client_schema['identifier']
    type_id = client_schema['type_identifier']
    assert response_client['type_identifier'] == type_id
    assert response_client['is_active'] == client_schema['is_active']


def test_get_client_by_id(
    session, db_client, api_client, superuser_token
) -> None:
    response = api_client.get(
        url=f'/clients/{db_client.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert UUID(data['id']) == db_client.id
    assert data['name'] == db_client.name
    assert data['client_type'] == db_client.client_type
    assert data['type_identifier'] == db_client.type_identifier
    assert data['identifier'] == db_client.identifier


def test_get_client_by_id_not_found(
    session, api_client, superuser_token
) -> None:
    response = api_client.get(
        url='/clients/123e4567-e89b-12d3-a456-426614174000',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}
