import pytest
from pydantic import ValidationError

from src.models import IdentifierType
from src.schemas.clients import ClientRequestCreate, ClientRequestUpdate


def test_client_create_valid_cpf():
    """Test that a valid CPF (11 digits) passes validation."""
    client = ClientRequestCreate(
        name='Test Client',
        client_type='individual',
        type_identifier=IdentifierType.cpf,
        identifier='12345678901',  # 11 digits
    )
    assert client.identifier == '12345678901'


def test_client_create_invalid_cpf():
    """Test that an invalid CPF (not 11 digits) fails validation."""
    with pytest.raises(ValidationError) as exc_info:
        ClientRequestCreate(
            name='Test Client',
            client_type='individual',
            type_identifier=IdentifierType.cpf,
            identifier='1234567890',  # 10 digits - too short
        )
    assert 'CPF must have exactly 11 digits' in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        ClientRequestCreate(
            name='Test Client',
            client_type='individual',
            type_identifier=IdentifierType.cpf,
            identifier='123456789012',  # 12 digits - too long
        )
    assert 'CPF must have exactly 11 digits' in str(exc_info.value)


def test_client_create_valid_cnpj():
    """Test that a valid CNPJ (14 digits) passes validation."""
    client = ClientRequestCreate(
        name='Test Company',
        client_type='business',
        type_identifier=IdentifierType.cnpj,
        identifier='12345678901234',  # 14 digits
    )
    assert client.identifier == '12345678901234'


def test_client_create_invalid_cnpj():
    """Test that an invalid CNPJ (not 14 digits) fails validation."""
    with pytest.raises(ValidationError) as exc_info:
        ClientRequestCreate(
            name='Test Company',
            client_type='business',
            type_identifier=IdentifierType.cnpj,
            identifier='1234567890123',  # 13 digits - too short
        )
    assert 'CNPJ must have exactly 14 digits' in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        ClientRequestCreate(
            name='Test Company',
            client_type='business',
            type_identifier=IdentifierType.cnpj,
            identifier='123456789012345',  # 15 digits - too long
        )
    assert 'CNPJ must have exactly 14 digits' in str(exc_info.value)


def test_client_update_valid_cpf():
    """Test that a valid CPF update passes validation."""
    client_update = ClientRequestUpdate(
        type_identifier=IdentifierType.cpf,
        identifier='12345678901',  # 11 digits
    )
    assert client_update.identifier == '12345678901'


def test_client_update_valid_cnpj():
    """Test that a valid CNPJ update passes validation."""
    client_update = ClientRequestUpdate(
        type_identifier=IdentifierType.cnpj,
        identifier='12345678901234',  # 14 digits
    )
    assert client_update.identifier == '12345678901234'


def test_client_update_invalid_cpf():
    """Test that an invalid CPF update fails validation."""
    with pytest.raises(ValidationError) as exc_info:
        ClientRequestUpdate(
            type_identifier=IdentifierType.cpf,
            identifier='1234567890',  # 10 digits - too short
        )
    assert 'CPF must have exactly 11 digits' in str(exc_info.value)


def test_client_update_invalid_cnpj():
    """Test that an invalid CNPJ update fails validation."""
    with pytest.raises(ValidationError) as exc_info:
        ClientRequestUpdate(
            type_identifier=IdentifierType.cnpj,
            identifier='1234567890123',  # 13 digits - too short
        )
    assert 'CNPJ must have exactly 14 digits' in str(exc_info.value)


def test_client_update_partial_no_identifier():
    """Test that a partial update without identifier passes validation."""
    client_update = ClientRequestUpdate(
        name='Updated Name',
        client_type='updated_type',
    )
    assert client_update.identifier is None
    assert client_update.name == 'Updated Name'


def test_client_update_partial_no_type():
    """Test that a partial update with identifier but no type passes
    validation."""
    client_update = ClientRequestUpdate(
        name='Updated Name',
        identifier='12345678901',  # We can't validate without knowing the type
    )
    assert client_update.identifier == '12345678901'
    assert client_update.type_identifier is None
