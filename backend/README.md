# Qontrola Backend

Um sistema ERP multi-tenant construído com FastAPI, SQLAlchemy e PostgreSQL.

## Multi-Tenant Architecture

This application implements a multi-tenant architecture with a shared database approach:

- Each tenant has its own isolated data but shares the same database and schema
- Tenants are identified by a unique domain
- All data is segregated by tenant_id in database queries
- JWT tokens include tenant information for secure authentication

## Soft Delete Pattern

This application implements a soft delete pattern:

- Records are never physically deleted from the database
- Instead, an `is_active` flag is set to `False` when a record is "deleted"
- By default, GET endpoints only return active records
- Add the query parameter `include_inactive=true` to include inactive records

This approach provides several benefits:
- Data can be recovered if deleted accidentally
- Historical data is preserved for auditing and analysis
- Referential integrity is maintained

### Key Features

- **Tenant Registration**: New organizations can register and create their first admin user
- **Tenant-Based Authorization**: Data access is strictly controlled by tenant boundaries
- **Role-Based Permissions**:
  - Superusers can manage all users within their tenant
  - Regular users can only manage their own information
- **Tenant Isolation**: All database queries include tenant filtering for data isolation
- **Brazilian Identifier Validation**: Automatic validation of CPF (11 digits) and CNPJ (14 digits) identifiers

## API Usage

### Authentication

All authenticated endpoints require:
1. A valid JWT token (via Bearer authentication)
2. A tenant domain header (`X-Tenant-Domain`)

### Tenant Registration

```
POST /tenants/register
```

Request body:
```json
{
  "name": "Organization Name",
  "domain": "organization-domain",
  "admin_user": {
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "secure_password"
  }
}
```

### User Authentication

```
POST /token
```

Headers:
```
X-Tenant-Domain: organization-domain
```

Form data:
- username: admin@example.com
- password: secure_password

### Client Management

Clients can be created with CPF or CNPJ identifiers:

```
POST /clients
```

Request body:
```json
{
  "name": "Client Name",
  "client_type": "type",
  "type_identifier": "cpf", // or "cnpj"
  "identifier": "12345678901" // 11 digits for CPF, 14 digits for CNPJ
}
```

### User Management

All user management endpoints follow these permission rules:
- Superusers can manage all users within their tenant
- Regular users can only view and modify their own data

## Development Setup

1. Install Poetry
2. Run `poetry install`
3. Set up your .env file
4. Run migrations with `poetry run alembic upgrade head`
5. Start the server with `poetry run task run`

## Running Migrations

After making model changes, generate a migration:

```bash
python create_migration.py
poetry run alembic upgrade head
```

## Documentation

Para documentação detalhada sobre a arquitetura e funcionalidades do backend, consulte:

- [Documentação Completa](docs/README.md) - Índice de toda a documentação do backend
- [Arquitetura do Backend](docs/backend_architecture.md) - Diagramas de arquitetura detalhados
- [Arquitetura Multi-tenant](docs/multi_tenant_architecture.md) - Detalhes da implementação multi-tenant
- [Autenticação e Segurança](docs/authentication_security.md) - Sistema de autenticação e práticas de segurança
- [Referência da API](docs/api_reference.md) - Documentação completa dos endpoints
