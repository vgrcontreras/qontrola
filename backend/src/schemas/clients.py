from uuid import UUID

from pydantic import BaseModel

from src.models import IdentifierType


class ClientRequestCreate(BaseModel):
    name: str
    client_type: str
    type_identifier: IdentifierType
    identifier: str

    # @field_validator('identifier')
    # def validate_identifier_length():
    #     ...


class ClientResponse(BaseModel):
    id: UUID
    name: str
    client_type: str
    type_identifier: IdentifierType
    identifier: str


class ClientRequestUpdate(BaseModel):
    name: str | None = None
    client_type: str | None = None
    type_identifier: IdentifierType | None = None
    identifier: str | None = None


class ClientListRequest(BaseModel):
    clients: list[ClientResponse]
