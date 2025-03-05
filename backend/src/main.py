# from .models import
from http import HTTPStatus

from fastapi import FastAPI

from src.routes import departments, users
from src.schemas.base import Message

app = FastAPI()

app.include_router(departments.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
