from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class User(BaseModel):
    id: int
    name: str
    last_name: str
    email: EmailStr


class DepartmentSchema(BaseModel):
    name: str


class DepartmentPublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class DepartmentPublicList(BaseModel):
    departments: list[DepartmentPublic]
