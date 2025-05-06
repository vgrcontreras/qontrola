# qontrola: Organize seus projetos e finanças sem complicação

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

Já foi prestador de serviço e sentiu dificuldade pra organizar as tarefas do projeto e entender, no fim das contas, quanto entrou e quanto saiu?  
A **qontrola** nasceu justamente dessa dor. Ela te ajuda a ter controle real sobre seus projetos, tarefas e finanças — tudo num só lugar.

Pensada para quem presta serviços por projeto (como agências, consultorias e freelancers), a qontrola une visão estratégica da empresa com o controle financeiro detalhado de cada entrega.

## 📌 Índice

- [Sobre o Projeto](#💡-sobre-o-projeto)
- [Funcionalidades](#✅-funcionalidades)
- [Exemplos de Uso](#🧩-exemplos-de-uso)
- [Tecnologias Utilizadas](#🔧-tecnologias-utilizadas)
- [Como Rodar o Projeto](#▶️-como-rodar-o-projeto)
- [Docker Setup](#🐳-docker-setup)
- [Modelagem de Dados](#🧠-modelagem-de-dados)
- [Documentação Técnica](#📚-documentação-técnica)

## 💡 Sobre o Projeto

Gerenciar tarefas já é complicado. Agora, somar isso ao controle financeiro por projeto... é o caos — e é aí que a maioria dos ERPs falha.

A qontrola veio resolver isso:  
💥 Nada de planilhas perdidas, informações soltas ou dashboards que ninguém entende.

A plataforma foi desenhada para te ajudar a responder perguntas como:
- Esse projeto está dando lucro?
- Onde estou gastando mais do que devia?
- Qual cliente está mais rentável?

### A qontrola te oferece:
- **Controle micro:** cada projeto tem seu próprio fluxo de caixa, receitas e despesas.
- **Visão macro:** veja como anda a empresa como um todo, com relatórios agregados e KPIs.
- **Interface simples:** ideal pra quem quer controlar o negócio sem ser expert em planilhas ou finanças.

## ✅ Funcionalidades

### Gestão de Projetos
- Cadastro com status, orçamento, prazos e milestones.
- Acompanhamento de orçamento previsto vs. realizado.

### Controle Financeiro
- Receita e despesa por projeto.
- Fluxo de caixa individual e consolidado.
- Categorias, centros de custo e tipos de despesa.

### Permissões e Acesso
- Perfis de usuário (admin, padrão).
- Autenticação com Supabase.
- Auditoria e histórico de alterações.

## 🧩 Exemplos de Uso

- Uma empresa cria sua conta e adiciona 5 membros.
- Cada colaborador acessa só os dados da própria empresa.
- Os projetos são organizados por departamento (TI, Design, Comercial).
- Cada setor consegue acompanhar seus próprios resultados.

---

## 🔧 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web de alta performance para APIs
- **SQLAlchemy** - ORM para interação com banco de dados
- **Pydantic** - Validação de dados e configurações
- **Alembic** - Migrações de banco de dados
- **Asyncpg** - Driver assíncrono para PostgreSQL
- **Uvicorn** - Servidor ASGI para Python
- **PyJWT** - Implementação de JSON Web Tokens
- **Argon2** - Algoritmo de hash seguro para senhas

### Frontend
- Em desenvolvimento

### Infraestrutura
- **Docker & Docker Compose** - Containerização e orquestração
- **PostgreSQL** - Banco de dados relacional
- **pgAdmin** - Ferramenta de administração para PostgreSQL

### Desenvolvimento e Qualidade
- **Poetry** - Gerenciamento de dependências Python
- **Pytest** - Framework de testes
- **Ruff** - Linter e formatador de código
- **Pre-commit** - Hooks de Git para garantir qualidade
- **MkDocs** - Geração de documentação
- **GitHub Actions** - CI/CD


## ▶️ Como Rodar o Projeto

### Usando Docker Compose

O projeto pode ser executado facilmente usando Docker Compose, que configurará automaticamente o ambiente com todos os serviços necessários.

```bash
# Clonar o repositório
git clone git@github.com:vgrcontreras/qontrola.git
cd qontrola

# Iniciar todos os serviços (backend, postgres, pgadmin)
docker compose up -d
```

Para interromper todos os serviços:
```bash
docker compose down
```

Para reconstruir e reiniciar os serviços (após alterações):
```bash
docker compose up -d --build
```

Para remover volumes também (cuidado: isso apagará dados persistentes):
```bash
docker compose down -v
```

### Acessando os Serviços

Após iniciar os serviços, você pode acessá-los através das seguintes URLs:

- **Backend API**: http://localhost:8000
- **pgAdmin**: http://localhost:5050

### Acessando o Banco de Dados via pgAdmin

1. Acesse pgAdmin em http://localhost:5050
2. Credenciais de acesso ao pgAdmin:
   - **Email**: admin@qontrola.com
   - **Senha**: admin

3. Para conectar ao servidor PostgreSQL:
   - Clique em "Add New Server"
   - Na aba "General", defina um nome para o servidor (ex: "qontrola")
   - Na aba "Connection", preencha:
     - **Host**: postgres
     - **Port**: 5432
     - **Maintenance database**: qontrola
     - **Username**: postgres
     - **Password**: postgres
   - Clique em "Save"

Agora você terá acesso ao banco de dados PostgreSQL através da interface do pgAdmin.

---

Para documentação mais detalhada sobre a configuração do Docker, incluindo solução de problemas, consulte [Docker Setup Documentation](docs/docker-setup.md).

## Documentação Técnica

Se você é desenvolvedor ou tem curiosidade sobre como funciona o backend da qontrola, temos uma documentação detalhada disponível:

- [Arquitetura do Backend](backend/docs/README.md) - Explore os diagramas e detalhes técnicos da implementação backend

Esta documentação inclui informações sobre a arquitetura multi-tenant, fluxos de autenticação, modelos de dados e endpoints da API.
