from fastapi import FastAPI

from src.api.routes import clients, departments, login, users

app = FastAPI()

app.include_router(departments.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(clients.router)
