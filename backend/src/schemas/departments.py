from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    message: str


class DepartmentSchema(BaseModel):
    name: str


class DepartmentPublic(BaseModel):
    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)


class DepartmentPublicList(BaseModel):
    departments: list[DepartmentPublic]
    model_config = ConfigDict(from_attributes=True)
