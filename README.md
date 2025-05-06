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

- **Python** (Pandas, SQLAlchemy, Pydantic, FastAPI)
- **SQL**
- **AWS** para serviços na nuvem
- **dbt** para transformação de dados
- **Streamlit** para criação de interfaces gráficas
- **Docker** para ambiente e deploy
- **Supabase** como backend as a service
- **Power BI** para visualizações interativas
- **Selenium** para automações web
- **Pydantic e Pandera** para qualidade de dados

---

## ▶️ Como Rodar o Projeto

```bash
git clone https://github.com/seu-usuario/qontrola.git
cd qontrola/backend


To remove volumes as well:
```bash
docker compose down -v
```

For more detailed documentation on the Docker setup, including troubleshooting, see [Docker Setup Documentation](docs/docker-setup.md).
