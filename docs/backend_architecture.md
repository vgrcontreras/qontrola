# 🧠 Arquitetura do Backend – Qontrola

Esta documentação descreve em detalhes a arquitetura e o funcionamento do backend do sistema **Qontrola**, uma aplicação construída com FastAPI, SQLAlchemy e PostgreSQL.

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Modelos de Dados](#modelos-de-dados)
- [Arquitetura de Rotas API](#arquitetura-de-rotas-api)
- [Diagrama de Componentes](#diagrama-de-componentes)
- [Fluxo de Autenticação](#fluxo-de-autenticação)
- [Diagrama de Relacionamento de Entidades](#diagrama-de-relacionamento-de-entidades)
- [Configuração e Execução](#configuração-e-execução)

## Visão Geral

O backend do Qontrola é construído com FastAPI, um framework moderno e de alto desempenho para Python. O sistema utiliza uma arquitetura multi-tenant com banco de dados compartilhado, onde cada tenant (inquilino) possui seus próprios dados isolados no mesmo banco de dados PostgreSQL.

### Principais Tecnologias

- **FastAPI**: Framework web para APIs REST
- **SQLAlchemy**: ORM (Object-Relational Mapping) para interação com o banco de dados
- **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional
- **Pydantic**: Validação de dados e serialização/deserialização
- **JWT**: Autenticação baseada em tokens

## Modelos de Dados

O diagrama abaixo ilustra os principais modelos de dados do sistema e seus relacionamentos:

```mermaid
classDiagram
    class Tenant {
        +UUID id
        +String name
        +String domain
        +Boolean is_active
        +DateTime created_at
        +DateTime updated_at
        +List~User~ users
        +List~Client~ clients
        +List~Project~ projects
        +List~Task~ tasks
    }

    class User {
        +UUID id
        +String email
        +String password
        +UUID tenant_id
        +String full_name
        +Boolean is_superuser
        +Boolean is_active
        +DateTime created_at
        +DateTime updated_at
    }

    class Client {
        +UUID id
        +String name
        +String client_type
        +IdentifierType type_identifier
        +String identifier
        +UUID tenant_id
        +DateTime created_at
        +DateTime update_at
        +DateTime updated_by
        +Boolean is_active
    }

    class Project {
        +UUID id
        +String name
        +UUID tenant_id
        +UUID created_by
        +String status_state
        +Float project_value
        +Date target_date
        +DateTime created_at
        +DateTime updated_at
        +UUID updated_by
        +Boolean is_active
        +List~Task~ tasks
    }

    class Task {
        +UUID id
        +String title
        +UUID project_id
        +UUID tenant_id
        +UUID created_by
        +String description
        +String status
        +String priority
        +Date due_date
        +DateTime created_at
        +DateTime updated_at
        +UUID updated_by
        +Boolean is_active
    }

    class IdentifierType {
        <<enumeration>>
        CPF
        CNPJ
    }

    Tenant "1" -- "*" User
    Tenant "1" -- "*" Client
    Tenant "1" -- "*" Project
    Tenant "1" -- "*" Task
    Project "1" -- "*" Task
```

### Descrição dos Modelos

- **Tenant**: Representa uma organização ou inquilino no sistema multi-tenant.
- **User**: Usuários do sistema associados a um tenant específico.
- **Client**: Clientes cadastrados por cada tenant, com suporte a identificadores brasileiros (CPF/CNPJ).
- **Project**: Projetos gerenciados pelo tenant, podendo conter múltiplas tarefas.
- **Task**: Tarefas associadas a um projeto específico.
- **IdentifierType**: Enumeração para os tipos de identificadores de clientes (CPF ou CNPJ).

Todos os modelos implementam o padrão de exclusão lógica (soft delete) através do campo `is_active`, permitindo a recuperação de dados e mantendo o histórico completo.

## Arquitetura de Rotas API

O diagrama abaixo mostra a estrutura das rotas da API e como elas se conectam aos serviços:

```mermaid
flowchart TD
    Client[Client] --> API[FastAPI App]

    subgraph API
        Main[main.py]
        Auth[Authentication]

        subgraph Routes
            TenantRoutes[Tenant Routes]
            UserRoutes[User Routes]
            LoginRoutes[Login Routes]
            ClientRoutes[Client Routes]
            ProjectRoutes[Project Routes]
            TaskRoutes[Task Routes]
            SuperuserRoutes[Superuser Routes]
        end

        subgraph Services
            DB[Database Service]
            Security[Security Service]
        end

        Main --> Routes
        Routes --> Services
        Auth --> Routes
    end

    API --> Database[(PostgreSQL)]
```

### Principais Rotas

- **/tenants**: Gerenciamento de tenants (inquilinos)
- **/users**: Gerenciamento de usuários
- **/token**: Autenticação e obtenção de tokens JWT
- **/clients**: Gerenciamento de clientes
- **/projects**: Gerenciamento de projetos
- **/tasks**: Gerenciamento de tarefas
- **/superuser**: Operações administrativas restritas a superusuários

Todas as rotas autenticadas requerem um token JWT válido e um cabeçalho com o domínio do tenant (`X-Tenant-Domain`).

## Diagrama de Componentes

O diagrama abaixo ilustra os principais componentes do sistema e suas interações:

```mermaid
flowchart TB
    subgraph Frontend
        WebApp[Web Application]
    end

    subgraph Backend
        subgraph API[FastAPI Application]
            Routes[API Routes]
            Schemas[Pydantic Schemas]
            Models[SQLAlchemy Models]
            Core[Core Components]
            Dependencies[Dependencies]
        end

        subgraph Database
            PostgreSQL[(PostgreSQL)]
        end

        Routes --> Dependencies
        Routes --> Schemas
        Dependencies --> Models
        Models --> PostgreSQL
        Core --> Models
    end

    WebApp <--> Routes
```

### Componentes Principais

- **Routes**: Definições das rotas da API FastAPI
- **Schemas**: Modelos Pydantic para validação de dados de entrada e saída
- **Models**: Modelos SQLAlchemy que representam as tabelas do banco de dados
- **Core**: Componentes centrais como configurações e serviços de banco de dados
- **Dependencies**: Dependências injetáveis do FastAPI para autenticação e acesso a recursos

## Fluxo de Autenticação

O diagrama de sequência abaixo ilustra o fluxo completo de autenticação:

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI
    participant Auth as Authentication
    participant DB as Database

    Client->>API: Login Request
    API->>Auth: Validate Credentials
    Auth->>DB: Query User
    DB-->>Auth: Return User Data
    Auth->>Auth: Verify Password
    Auth-->>API: Generate JWT Token
    API-->>Client: Return Token

    Client->>API: Request with Token
    API->>Auth: Validate Token
    Auth-->>API: Token Valid
    API->>DB: Query Data
    DB-->>API: Return Data
    API-->>Client: Return Response
```

### Processo de Autenticação

1. O cliente envia um pedido de login com email e senha para a rota `/token`
2. A API valida as credenciais, verificando o usuário no banco de dados
3. Se as credenciais forem válidas, um token JWT é gerado e retornado
4. Para requisições subsequentes, o cliente envia o token JWT no cabeçalho Authorization
5. A API valida o token e verifica o acesso ao recurso solicitado
6. Se o token for válido e o usuário tiver permissão, a API processa a solicitação

O token JWT inclui informações sobre o tenant e as permissões do usuário, garantindo a isolação de dados.

## Diagrama de Relacionamento de Entidades

Este diagrama mostra as relações entre as entidades no banco de dados:

```mermaid
erDiagram
    TENANT ||--o{ USER : has
    TENANT ||--o{ CLIENT : has
    TENANT ||--o{ PROJECT : has
    TENANT ||--o{ TASK : has
    PROJECT ||--o{ TASK : contains

    TENANT {
        uuid id PK
        string name
        string domain
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    USER {
        uuid id PK
        string email
        string password
        uuid tenant_id FK
        string full_name
        boolean is_superuser
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    CLIENT {
        uuid id PK
        string name
        string client_type
        enum type_identifier
        string identifier
        uuid tenant_id FK
        datetime created_at
        datetime update_at
        datetime updated_by
        boolean is_active
    }

    PROJECT {
        uuid id PK
        string name
        uuid tenant_id FK
        uuid created_by
        string status_state
        float project_value
        date target_date
        datetime created_at
        datetime updated_at
        uuid updated_by
        boolean is_active
    }

    TASK {
        uuid id PK
        string title
        uuid project_id FK
        uuid tenant_id FK
        uuid created_by
        string description
        string status
        string priority
        date due_date
        datetime created_at
        datetime updated_at
        uuid updated_by
        boolean is_active
    }
```

Este diagrama ER mostra:
- Cada TENANT pode ter muitos USERs, CLIENTs, PROJECTs e TASKs
- Cada PROJECT pode ter muitas TASKs
- Todas as entidades principais (USER, CLIENT, PROJECT, TASK) estão associadas a um TENANT

## Configuração e Execução

### Requisitos

- Python 3.9+
- Poetry (gerenciador de dependências)
- PostgreSQL

### Configuração do Ambiente

1. Clone o repositório
2. Instale as dependências com Poetry:
   ```
   poetry install
   ```
3. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/qontrola
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

### Migrações do Banco de Dados

Após fazer alterações nos modelos, gere uma migração:

```bash
python create_migration.py
poetry run alembic upgrade head
```

### Execução do Servidor

Inicie o servidor FastAPI com:

```bash
poetry run uvicorn src.api.main:app --reload
```

O servidor estará disponível em `http://localhost:8000` e a documentação interativa da API em `http://localhost:8000/docs`.

---

Esta documentação fornece uma visão geral completa da arquitetura do backend do Qontrola. Para informações específicas sobre funcionalidades como a validação de identificadores brasileiros, consulte a documentação adicional disponível na pasta `docs/`. 