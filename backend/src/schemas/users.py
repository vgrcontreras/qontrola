from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_superuser: bool = False
    tenant_id: UUID


class UserPublic(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    is_superuser: bool
    is_active: bool
    tenant_id: UUID
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    tenant_id: UUID | None = None


class PasswordChange(BaseModel):
    password: str
    password_confirmation: str
