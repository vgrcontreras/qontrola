# Implementação da Funcionalidade de Categorias

Data: 2023-05-15

## Resumo

Adicionamos a capacidade de categorizar projetos e tarefas através de uma nova entidade `Category`. Esta funcionalidade permite organizar os dados do sistema de forma mais eficiente e facilitar consultas e relatórios.

## Mudanças Realizadas

### 1. Novo Modelo de Dados

Criamos um novo modelo `Category` com os seguintes campos:
- `id`: Identificador único (UUID)
- `name`: Nome da categoria
- `tenant_id`: Associação ao tenant
- `created_at`, `updated_at`: Timestamps de criação e atualização
- `is_active`: Indicador de status da categoria

### 2. Novas Relações

Adicionamos relações aos modelos existentes:
- Projetos podem ter uma categoria opcional
- Tarefas podem ter uma categoria opcional
- Categorias pertencem a um tenant
- Um tenant pode ter múltiplas categorias

### 3. Novos Endpoints

Implementamos os seguintes endpoints para gerenciar categorias:
- `GET /categories`: Listar todas as categorias do tenant
- `GET /categories/{category_id}`: Obter uma categoria específica
- `POST /categories`: Criar uma nova categoria
- `DELETE /categories/{category_id}`: Desativar uma categoria existente

### 4. Integração com Projetos e Tarefas

Modificamos os endpoints de projetos e tarefas para suportar a associação com categorias:
- Adicionamos o campo `category_name` aos schemas de criação e atualização
- Implementamos a lógica para criar a categoria automaticamente se não existir
- Atualizamos os schemas de resposta para incluir o campo `category_id`

### 5. Função Utilitária

Criamos uma função utilitária chamada `get_or_create_category` que:
- Busca uma categoria existente pelo nome e tenant_id
- Cria uma nova categoria se não encontrar
- Normaliza o nome da categoria removendo espaços extras
- Retorna a categoria encontrada ou criada

## Arquivos Modificados

- `src/models.py`: Adicionado modelo `Category` e relações
- `src/schemas/categories.py`: Criado schemas para categorias
- `src/schemas/projects.py`: Adicionado suporte a categorias
- `src/schemas/tasks.py`: Adicionado suporte a categorias
- `src/api/routes/categories.py`: Implementado endpoints para categorias
- `src/api/routes/projects.py`: Adicionado lógica de integração com categorias
- `src/api/routes/tasks.py`: Adicionado lógica de integração com categorias
- `src/api/main.py`: Registrado as rotas de categorias
- `src/utils/category_utils.py`: Implementado função utilitária

## Benefícios

1. **Organização Melhorada**: Permite agrupar projetos e tarefas em categorias lógicas
2. **Filtragem Facilitada**: Possibilita filtrar por categoria no futuro
3. **Isolamento de Dados**: Mantém as categorias isoladas por tenant
4. **Flexibilidade**: Criação automática de categorias sob demanda
5. **API Consistente**: Mantém os mesmos padrões REST do resto da aplicação

## Próximos Passos

1. Implementar filtragem de projetos e tarefas por categoria
2. Adicionar endpoints para buscar projetos/tarefas por categoria
3. Considerar a adição de cores ou outros metadados às categorias
4. Adicionar suporte a subcategorias, se necessário 