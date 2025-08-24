from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from src.models import IdentifierType

# Constants for identifier lengths
CPF_LENGTH = 11
CNPJ_LENGTH = 14


class ClientRequestCreate(BaseModel):
    name: str
    client_type: str
    type_identifier: IdentifierType
    identifier: str

    @field_validator('identifier')
    def validate_identifier_length(cls, value, info):
        type_identifier = info.data.get('type_identifier')

        if type_identifier == IdentifierType.cpf and len(value) != CPF_LENGTH:
            raise ValueError('CPF must have exactly 11 digits')

        if (
            type_identifier == IdentifierType.cnpj
            and len(value) != CNPJ_LENGTH
        ):
            raise ValueError('CNPJ must have exactly 14 digits')

        return value


class ClientResponse(BaseModel):
    id: UUID
    name: str
    client_type: str
    type_identifier: IdentifierType
    identifier: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ClientRequestUpdate(BaseModel):
    name: str | None = None
    client_type: str | None = None
    type_identifier: IdentifierType | None = None
    identifier: str | None = None

    @field_validator('identifier')
    def validate_identifier_length(cls, value, info):
        if value is None:
            return value

        type_identifier = info.data.get('type_identifier')

        # If type_identifier is not provided in the update, we can't validate
        if type_identifier is None:
            return value

        if type_identifier == IdentifierType.cpf and len(value) != CPF_LENGTH:
            raise ValueError('CPF must have exactly 11 digits')

        if (
            type_identifier == IdentifierType.cnpj
            and len(value) != CNPJ_LENGTH
        ):
            raise ValueError('CNPJ must have exactly 14 digits')

        return value


class ClientListRequest(BaseModel):
    clients: list[ClientResponse]
