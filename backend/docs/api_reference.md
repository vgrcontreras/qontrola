# API Reference - Qontrola Backend

Este documento descreve em detalhes os endpoints disponíveis na API do Qontrola.

## Base URL

```
http://localhost:8000
```

Para ambientes de produção, utilize o domínio apropriado.

## Autenticação

A maioria dos endpoints requer autenticação. O sistema utiliza autenticação baseada em tokens JWT (JSON Web Tokens).

### Obter Token de Acesso

```
POST /token
```

**Headers**:
```
X-Tenant-Domain: domain-do-tenant
```

**Form Data**:
- `username`: Email do usuário
- `password`: Senha do usuário

**Resposta**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usando o Token

Para endpoints autenticados, inclua o token no cabeçalho da requisição:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
X-Tenant-Domain: domain-do-tenant
```

## Endpoints

### Tenants

#### Registrar Novo Tenant

```
POST /tenants/register
```

**Corpo**:
```json
{
  "name": "Nome da Organização",
  "domain": "dominio-organizacao",
  "admin_user": {
    "email": "admin@exemplo.com",
    "password": "senha_segura",
    "full_name": "Nome do Admin"
  }
}
```

#### Listar Tenants (Apenas Superusuários)

```
GET /superuser/tenants
```

### Usuários

#### Listar Usuários

```
GET /users
```

#### Obter Usuário

```
GET /users/{user_id}
```

#### Criar Usuário

```
POST /users
```

**Corpo**:
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha_segura",
  "full_name": "Nome do Usuário",
  "is_superuser": false
}
```

#### Atualizar Usuário

```
PUT /users/{user_id}
```

**Corpo**:
```json
{
  "email": "novo-email@exemplo.com",
  "full_name": "Novo Nome",
  "is_superuser": false,
  "is_active": true
}
```

#### Alterar Senha

```
PUT /users/{user_id}/password
```

**Corpo**:
```json
{
  "current_password": "senha_atual",
  "new_password": "nova_senha"
}
```

#### Desativar Usuário

```
DELETE /users/{user_id}
```

### Clientes

#### Listar Clientes

```
GET /clients
```

Parâmetros de query:
- `include_inactive`: Incluir clientes inativos (opcional, padrão: false)

#### Obter Cliente

```
GET /clients/{client_id}
```

#### Criar Cliente

```
POST /clients
```

**Corpo**:
```json
{
  "name": "Nome do Cliente",
  "client_type": "tipo",
  "type_identifier": "cpf", // ou "cnpj"
  "identifier": "12345678901" // 11 dígitos para CPF, 14 para CNPJ
}
```

#### Atualizar Cliente

```
PUT /clients/{client_id}
```

**Corpo**:
```json
{
  "name": "Novo Nome do Cliente",
  "client_type": "novo-tipo",
  "is_active": true
}
```

#### Desativar Cliente

```
DELETE /clients/{client_id}
```

### Projetos

#### Listar Projetos

```
GET /projects
```

Parâmetros de query:
- `include_inactive`: Incluir projetos inativos (opcional, padrão: false)

#### Obter Projeto

```
GET /projects/{project_id}
```

#### Criar Projeto

```
POST /projects
```

**Corpo**:
```json
{
  "name": "Nome do Projeto",
  "status_state": "em-andamento",
  "project_value": 10000.0,
  "target_date": "2023-12-31"
}
```

#### Atualizar Projeto

```
PUT /projects/{project_id}
```

**Corpo**:
```json
{
  "name": "Novo Nome do Projeto",
  "status_state": "concluido",
  "project_value": 12000.0,
  "target_date": "2024-01-15",
  "is_active": true
}
```

#### Desativar Projeto

```
DELETE /projects/{project_id}
```

### Tarefas

#### Listar Tarefas

```
GET /tasks
```

Parâmetros de query:
- `project_id`: Filtrar por projeto (opcional)
- `status`: Filtrar por status (opcional)
- `include_inactive`: Incluir tarefas inativas (opcional, padrão: false)

#### Obter Tarefa

```
GET /tasks/{task_id}
```

#### Criar Tarefa

```
POST /tasks
```

**Corpo**:
```json
{
  "title": "Título da Tarefa",
  "project_id": "uuid-do-projeto",
  "description": "Descrição detalhada da tarefa",
  "status": "to_do", // to_do, in_progress, done
  "priority": "medium", // low, medium, high
  "due_date": "2023-12-15"
}
```

#### Atualizar Tarefa

```
PUT /tasks/{task_id}
```

**Corpo**:
```json
{
  "title": "Novo Título da Tarefa",
  "description": "Nova descrição",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2023-12-20",
  "is_active": true
}
```

#### Desativar Tarefa

```
DELETE /tasks/{task_id}
```

## Formato de Resposta

Todas as respostas da API são retornadas em formato JSON.

## Tratamento de Erros

As respostas de erro incluirão uma mensagem de erro e o código de status HTTP apropriado.

Exemplo de resposta de erro:

```json
{
  "detail": "Não encontrado"
}
```

---

Para mais informações sobre a arquitetura e funcionamento do backend, consulte a [Documentação de Arquitetura do Backend](backend_architecture.md). 