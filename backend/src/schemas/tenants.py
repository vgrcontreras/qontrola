from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class TenantSchema(BaseModel):
    name: str
    domain: str

    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v):
        v = v.lower().strip().replace(' ', '-')
        return v


class TenantCreate(TenantSchema):
    pass


class TenantPublic(TenantSchema):
    id: UUID
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class TenantList(BaseModel):
    tenants: list[TenantPublic]


class TenantUpdate(BaseModel):
    name: str | None = None
    domain: str | None = None
    is_active: bool | None = None

    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v):
        if v is not None:
            v = v.lower().strip().replace(' ', '-')
        return v


class AdminUserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class TenantRegistration(TenantCreate):
    admin_user: AdminUserCreate
