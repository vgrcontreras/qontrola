#!/bin/bash

# Wait for the database to be ready
echo "Running database migrations"
alembic upgrade head

# Create admin user
echo "Creating admin user"
python -m src.initial_data

# Run the FastAPI application
echo "Starting FastAPI application"
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload


