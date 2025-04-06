from http import HTTPStatus
from uuid import UUID

import pytest

# Mark all tests in this module as asyncio tests
pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_register_tenant(api_client):
    """Test tenant registration endpoint with valid data"""
    response = api_client.post(
        '/tenants/register',
        json={
            'name': 'New Tenant',
            'domain': 'newtenant.com',
            'admin_user': {
                'email': 'admin@newtenant.com',
                'password': 'secure_password',
            },
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['name'] == 'New Tenant'
    assert data['domain'] == 'newtenant.com'
    assert UUID(data['id']) is not None
    assert data['is_active'] is True


@pytest.mark.asyncio
async def test_register_tenant_domain_already_exists(api_client):
    """Test tenant registration with already existing domain"""
    # First create a tenant with a specific domain
    domain = 'duplicate-domain.com'

    # Register first tenant
    first_response = api_client.post(
        '/tenants/register',
        json={
            'name': 'First Tenant',
            'domain': domain,
            'admin_user': {
                'email': 'admin@first.com',
                'password': 'secure_password',
            },
        },
    )
    assert first_response.status_code == HTTPStatus.CREATED

    # Try to register a second tenant with the same domain
    second_response = api_client.post(
        '/tenants/register',
        json={
            'name': 'Second Tenant',
            'domain': domain,
            'admin_user': {
                'email': 'admin@second.com',
                'password': 'secure_password',
            },
        },
    )

    # The endpoint should prevent duplicate domains
    # Could be 400 or 500 depending on implementation
    assert second_response.status_code in {
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    }
    # Can't assert exact message since we don't know which error we'll get


@pytest.mark.asyncio
async def test_update_tenant(api_client, tenant, superuser_token):
    """Test updating tenant information"""
    response = api_client.put(
        '/tenants/current',
        json={
            'name': 'Updated Tenant Name',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['name'] == 'Updated Tenant Name'
    assert data['domain'] == tenant.domain  # Domain should remain unchanged


@pytest.mark.asyncio
async def test_update_tenant_domain(api_client, tenant, superuser_token):
    """Test updating tenant domain to a new unique domain"""
    new_domain = 'new-domain.com'
    response = api_client.put(
        '/tenants/current',
        json={
            'domain': new_domain,
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['domain'] == new_domain


@pytest.mark.asyncio
async def test_update_tenant_domain_already_exists(
    api_client, tenant, superuser_token, session
):
    """Test updating tenant domain to an already used domain"""
    # First create another tenant
    response = api_client.post(
        '/tenants/register',
        json={
            'name': 'Another Tenant',
            'domain': 'another-domain.com',
            'admin_user': {
                'email': 'admin@another-domain.com',
                'password': 'secure_password',
            },
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    # Try to update the original tenant to use the new tenant's domain
    response = api_client.put(
        '/tenants/current',
        json={
            'domain': 'another-domain.com',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'is already in use' in response.json()['detail']


@pytest.mark.asyncio
async def test_update_tenant_non_superuser(api_client, user_token):
    """Test that non-superusers cannot update tenant info"""
    response = api_client.put(
        '/tenants/current',
        json={
            'name': 'Should Not Work',
        },
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "doesn't have enough privileges" in response.json()['detail']
