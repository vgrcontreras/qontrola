# Documentação do Backend do Qontrola

Bem-vindo à documentação do backend do Qontrola. Esta seção contém informações detalhadas sobre a arquitetura, estrutura e funcionalidades do sistema backend.

## Páginas de Documentação

- [Arquitetura do Backend](backend_architecture.md) - Documentação detalhada sobre a arquitetura do sistema, incluindo diagramas explicativos
- [Arquitetura Multi-tenant](multi_tenant_architecture.md) - Explicação detalhada da implementação multi-tenant
- [Autenticação e Segurança](authentication_security.md) - Detalhes sobre o sistema de autenticação e práticas de segurança
- [Referência da API](api_reference.md) - Documentação completa dos endpoints da API
- [Validação de Identificadores Brasileiros](client_identifier_validation.md) - Detalhes sobre a implementação de validação de CPF e CNPJ

## Visão Geral

O backend do Qontrola é implementado como uma API REST usando FastAPI, um framework moderno e de alta performance para Python. O sistema utiliza uma arquitetura multi-tenant com banco de dados compartilhado, permitindo que múltiplas organizações utilizem a mesma instância do aplicativo com isolamento completo de dados.

### Principais Características:

- **Arquitetura Multi-tenant**: Isolamento de dados entre diferentes organizações
- **Autenticação JWT**: Sistema seguro de autenticação baseado em tokens
- **Padrão de Exclusão Lógica**: Preservação de dados históricos através de soft delete
- **Validação Avançada de Dados**: Utilizando Pydantic para garantir integridade dos dados
- **Controle de Acesso Baseado em Funções**: Diferentes níveis de permissão para usuários

Consulte a documentação de [Arquitetura do Backend](backend_architecture.md) para informações mais detalhadas sobre a estrutura e funcionamento do sistema. 