from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    full_name: str | None = None
    email: EmailStr
    password: str
    is_superuser: bool = False
    tenant_id: UUID | None = None


class UserPublic(BaseModel):
    id: UUID
    full_name: str | None = None
    email: EmailStr
    is_superuser: bool
    is_active: bool
    tenant_id: UUID
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class UserUpdate(BaseModel):
    full_name: str | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None
    email: EmailStr | None = None
    tenant_id: UUID | None = None


class PasswordChange(BaseModel):
    password: str
    password_confirmation: str
