# API de Categorias

Este documento descreve a funcionalidade de categorias adicionada ao sistema Qontrola.

## Visão Geral

A funcionalidade de categorias permite organizar projetos e tarefas em grupos lógicos, facilitando a filtragem, pesquisa e relatórios. Cada categoria pertence a um único tenant, garantindo o isolamento entre diferentes organizações.

### Características Principais

- Categorias são específicas por tenant (isolamento de dados)
- Uma categoria pode ser associada a múltiplos projetos e tarefas
- Projetos e tarefas podem ter no máximo uma categoria
- Criação automática de categorias sob demanda

## Modelo de Dados

A categoria é representada pelo seguinte modelo:

```python
class Category:
    id: UUID             # Identificador único
    name: str            # Nome da categoria (único por tenant)
    tenant_id: UUID      # Referência ao tenant ao qual pertence
    is_active: bool      # Status de ativação (default: True)
    created_at: datetime # Data de criação
    updated_at: datetime # Data de atualização
```

## Endpoints da API

### Listar Categorias

```
GET /categories
```

**Headers**:
```
Authorization: Bearer {token}
X-Tenant-Domain: {domain-do-tenant}
```

**Resposta**:
```json
{
  "categories": [
    {
      "id": "uuid-da-categoria",
      "name": "Marketing",
      "tenant_id": "uuid-do-tenant",
      "created_at": "2023-05-15T10:30:00Z",
      "updated_at": "2023-05-15T10:30:00Z",
      "is_active": true
    },
    {
      "id": "uuid-da-categoria-2",
      "name": "Desenvolvimento",
      "tenant_id": "uuid-do-tenant",
      "created_at": "2023-05-15T11:30:00Z",
      "updated_at": "2023-05-15T11:30:00Z",
      "is_active": true
    }
  ]
}
```

### Obter Categoria por ID

```
GET /categories/{category_id}
```

**Headers**:
```
Authorization: Bearer {token}
X-Tenant-Domain: {domain-do-tenant}
```

**Resposta**:
```json
{
  "id": "uuid-da-categoria",
  "name": "Marketing",
  "tenant_id": "uuid-do-tenant",
  "created_at": "2023-05-15T10:30:00Z",
  "updated_at": "2023-05-15T10:30:00Z",
  "is_active": true
}
```

### Criar Categoria

```
POST /categories
```

**Headers**:
```
Authorization: Bearer {token}
X-Tenant-Domain: {domain-do-tenant}
```

**Corpo**:
```json
{
  "name": "Nova Categoria"
}
```

**Resposta**:
```json
{
  "id": "uuid-da-nova-categoria",
  "name": "Nova Categoria",
  "tenant_id": "uuid-do-tenant",
  "created_at": "2023-05-15T12:30:00Z",
  "updated_at": "2023-05-15T12:30:00Z",
  "is_active": true
}
```

### Desativar Categoria

```
DELETE /categories/{category_id}
```

**Headers**:
```
Authorization: Bearer {token}
X-Tenant-Domain: {domain-do-tenant}
```

**Resposta**:
```json
{
  "message": "Category deleted"
}
```

## Integração com Projetos e Tarefas

A funcionalidade de categorias é integrada aos endpoints de projetos e tarefas, permitindo associar uma categoria durante a criação ou atualização.

### Criar Projeto com Categoria

```
POST /projects
```

**Corpo**:
```json
{
  "name": "Novo Projeto",
  "status_state": "active",
  "project_value": 1000.0,
  "target_date": "2023-12-31",
  "category_name": "Marketing"
}
```

Se a categoria "Marketing" não existir, ela será criada automaticamente.

### Atualizar Projeto com Categoria

```
PATCH /projects/{project_id}
```

**Corpo**:
```json
{
  "category_name": "Desenvolvimento"
}
```

### Criar Tarefa com Categoria

```
POST /tasks
```

**Corpo**:
```json
{
  "title": "Nova Tarefa",
  "description": "Descrição da tarefa",
  "status": "to_do",
  "priority": "medium",
  "due_date": "2023-06-30",
  "project_id": "uuid-do-projeto",
  "category_name": "Marketing"
}
```

### Atualizar Tarefa com Categoria

```
PATCH /tasks/{task_id}
```

**Corpo**:
```json
{
  "category_name": "Desenvolvimento"
}
```

## Função Utilitária

A função `get_or_create_category` é usada internamente para obter uma categoria existente ou criar uma nova se não existir.

```python
async def get_or_create_category(
    db: AsyncSession, 
    category_name: str, 
    tenant_id: uuid.UUID
) -> Optional[Category]
```

### Comportamento

1. Se `category_name` for nulo ou vazio, retorna `None`
2. Normaliza o nome da categoria removendo espaços em branco extras
3. Busca a categoria pelo nome e tenant_id
4. Se encontrar, retorna a categoria existente
5. Se não encontrar, cria uma nova categoria e retorna

## Considerações Importantes

1. Os nomes das categorias são normalizados (espaços extras removidos) antes do armazenamento e da busca
2. Cada tenant possui seu próprio conjunto de categorias isolado dos demais
3. O campo `category_name` é opcional em projetos e tarefas
4. Ao atualizar um projeto ou tarefa com uma nova categoria, a associação anterior é substituída 