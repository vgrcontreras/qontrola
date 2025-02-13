# from .models import
from http import HTTPStatus

from fastapi import FastAPI

from backend.schemas import User

app = FastAPI()


@app.get('/')
def hello_world():
    return {'Hello': 'World'}


@app.post('/', status_code=HTTPStatus.CREATED)
def create_user(user: User) -> None:
    return {'name': user.name, 'last_name': user.last_name}
