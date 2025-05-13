from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import (
                            categories,
                            clients,
                            login,
                            projects,
                            superuser,
                            tasks,
                            tenants,
                            users,
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000',  # Default React port
        'http://localhost:8080',
        'http://localhost:8081',  # Vite default port
        'http://localhost:5173',  # Another common Vite port
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(tenants.router, prefix='/tenants', tags=['tenants'])
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(login.router, prefix='/token', tags=['token'])
app.include_router(clients.router, prefix='/clients', tags=['clients'])
app.include_router(projects.router, prefix='/projects', tags=['projects'])
app.include_router(tasks.router, prefix='/tasks', tags=['tasks'])
app.include_router(
    categories.router, prefix='/categories', tags=['categories']
)
app.include_router(superuser.router, prefix='/superuser', tags=['superuser'])
