from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    salary: float
    is_superuser: bool = False


class UserPublic(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_superuser: bool
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class UserPublicSalary(UserPublic):
    salary: float
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    salary: float | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None
