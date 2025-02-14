from pydantic import BaseModel, EmailStr


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
