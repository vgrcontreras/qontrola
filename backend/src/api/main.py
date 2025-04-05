from fastapi import FastAPI

from src.api.routes import clients, login, projects, superuser, tenants, users

app = FastAPI()

app.include_router(tenants.router, prefix='/tenants', tags=['tenants'])
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(login.router, prefix='/token', tags=['token'])
app.include_router(clients.router, prefix='/clients', tags=['clients'])
app.include_router(projects.router, prefix='/projects', tags=['projects'])
app.include_router(superuser.router, prefix='/superuser', tags=['superuser'])
