# Qontrola Backend

A comprehensive ERP system built with FastAPI, SQLAlchemy, and PostgreSQL.

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Development Setup](#development-setup)
- [Running Migrations](#running-migrations)
- [Accessing the Application](#accessing-the-application)
- [Environment Variables](#environment-variables)
- [Documentation](#documentation)

## Architecture

This application implements a single-tenant architecture:

- All users and data belong to a single organization
- Simplified authentication without tenant isolation
- Direct access to all resources without tenant filtering
- JWT tokens contain user information for secure authentication

[↑ Back to top](#table-of-contents)



## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **SQLAlchemy ORM**: Powerful and flexible ORM for database operations
- **PostgreSQL Database**: Robust relational database with UUID support
- **JWT Authentication**: Secure token-based authentication
- **Automatic API Documentation**: Swagger UI available at `/docs`
- **Input Validation**: Pydantic models for request/response validation
- **User Management**: Create and manage users with role-based permissions
- **Role-Based Permissions**:
  - Superusers can manage all users and system resources
  - Regular users can only manage their own information
- **Client Management**: Manage clients with Brazilian identifier validation
- **Project Management**: Create and track projects with categories
- **Task Management**: Create and assign tasks to projects
- **Category System**: Organize projects and tasks with categories
- **Brazilian Business Logic**: CPF/CNPJ validation for Brazilian clients
- **Soft Delete**: Safe deletion with recovery capabilities
- **Role-Based Access**: Different permission levels for users

[↑ Back to top](#table-of-contents)

## Prerequisites

Before running the application, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)

[↑ Back to top](#table-of-contents)

## Quick Start with Docker Compose

The easiest way to get Qontrola Backend up and running is using Docker Compose. This will start all required services including PostgreSQL database, pgAdmin, and the FastAPI backend.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd qontrola/backend
```

### 2. Start All Services

```bash
docker-compose up -d
```

This command will:
- Pull and start a PostgreSQL 16 database
- Start pgAdmin for database management
- Build and start the FastAPI backend application
- Set up all necessary networking between services

### 3. Verify Services

Check that all services are running:

```bash
docker-compose ps
```

You should see three services running:
- `postgres` - PostgreSQL database (port 5432)
- `pgadmin` - Database administration tool (port 5050)
- `backend` - FastAPI application (port 8000)

### 4. Initialize the Database

The application will automatically run migrations and create the initial superuser on startup.

### 5. Stop Services

To stop all services:

```bash
docker-compose down
```

To stop services and remove volumes (⚠️ this will delete all data):

```bash
docker-compose down -v
```

[↑ Back to top](#table-of-contents)

## Development Setup

For local development without Docker:

### 1. Install Dependencies

Install Python 3.11+ and Poetry:

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 2. Database Setup

Start PostgreSQL using Docker:

```bash
docker-compose up postgres -d
```

### 3. Environment Configuration

Create a `.env` file in the backend directory:

```bash
cp .env-example .env
```

Edit the `.env` file with your configuration (see [Environment Variables](#environment-variables) section).

### 4. Database Migration

Run database migrations:

```bash
poetry run alembic upgrade head
```

### 5. Start Development Server

```bash
poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

[↑ Back to top](#table-of-contents)

## Running Migrations

### With Docker Compose

Migrations run automatically when starting the backend service. To run migrations manually:

```bash
docker-compose exec backend poetry run alembic upgrade head
```

### Local Development

After making model changes:

```bash
# Generate migration
poetry run alembic revision --autogenerate -m "Description of changes"

# Apply migration
poetry run alembic upgrade head
```

[↑ Back to top](#table-of-contents)

## Accessing the Application

Once the services are running, you can access:

### FastAPI Backend
- **API Base URL**: http://localhost:8000
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc

### Database Administration
- **pgAdmin**: http://localhost:5050
  - Email: `admin@qontrola.com`
  - Password: `admin`

### Database Connection
- **Host**: localhost (or `postgres` when connecting from within Docker)
- **Port**: 5432
- **Database**: qontrola
- **Username**: postgres
- **Password**: postgres

### Default Superuser
The application creates a default superuser on first startup:
- **Email**: `admin@example.com`
- **Password**: `admin`

⚠️ **Important**: Change the default superuser password in production!

[↑ Back to top](#table-of-contents)

## Documentation

For detailed documentation about the backend architecture and features, see:

- [Complete Documentation](docs/README.md) - Index of all backend documentation
- [Backend Architecture](docs/backend_architecture.md) - Detailed architecture diagrams
- [Authentication & Security](docs/authentication_security.md) - Authentication system and security practices
- [API Reference](docs/api_reference.md) - Complete endpoint documentation

[↑ Back to top](#table-of-contents)

## Environment Variables

The application uses the following environment variables:

### Docker Compose (Configured automatically)
When using Docker Compose, these variables are set automatically in the `docker-compose.yml` file:

```yaml
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/qontrola
SECRET_KEY=your_secret_key_here_please_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin
```

### Local Development (.env file)
For local development, create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/qontrola
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin_password
```

### Variable Descriptions
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token encryption (⚠️ Change in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time
- `ALGORITHM`: JWT encryption algorithm
- `FIRST_SUPERUSER_EMAIL`: Email for the initial superuser account
- `FIRST_SUPERUSER_PASSWORD`: Password for the initial superuser account

[↑ Back to top](#table-of-contents)
