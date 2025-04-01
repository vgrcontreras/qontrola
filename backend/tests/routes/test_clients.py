from http import HTTPStatus
from uuid import UUID


def test_create_client(api_client, superuser_token) -> None:
    response = api_client.post(
        url='/clients',
        json={
            'name': 'client1',
            'client_type': 'velas',
            'type_identifier': 'cnpj',
            'identifier': 'test',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['name'] == 'client1'
    assert data['client_type'] == 'velas'
    assert data['type_identifier'] == 'cnpj'
    assert data['identifier'] == 'test'
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
            'identifier': 'test',
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

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': "Client doesn't exists"}


def test_update_client_not_found(api_client, superuser_token) -> None:
    response = api_client.patch(
        url='/clients/123e4567-e89b-12d3-a456-426614174000',
        json={'name': 'test_update_name'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
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
    assert data['identifier'] == 'test'
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
            'identifier': 'test2',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    response = api_client.patch(
        url=f'/clients/{db_client.id}',
        json={'identifier': 'test2'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Client already exists'}


def test_get_all_clients(session, api_client) -> None:
    response = api_client.get(url='/clients')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'clients': []}


def test_get_client_by_id(session, db_client, api_client) -> None:
    response = api_client.get(url=f'/clients/{db_client.id}')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert UUID(data['id']) == db_client.id
    assert data['name'] == db_client.name
    assert data['client_type'] == db_client.client_type
    assert data['type_identifier'] == db_client.type_identifier
    assert data['identifier'] == db_client.identifier


def test_get_client_by_id_not_found(session, api_client) -> None:
    response = api_client.get(
        url='/clients/123e4567-e89b-12d3-a456-426614174000'
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Client not found'}
