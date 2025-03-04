# from .models import
from http import HTTPStatus

from fastapi import FastAPI

from src.routes import departments
from src.schemas import Message

app = FastAPI()

app.include_router(departments.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
