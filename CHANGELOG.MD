# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.



## [0.2.0] - 2026-11-27 (Parcial 2)

### Adicionado
- Banco de dados MySQL 8.4 em container Docker (`docker-compose.yml`), com
  volume para persistência. As credenciais ficam no `.env` (fora do Git), e o
  `.env.example` documenta as variáveis necessárias.
- Configuração centralizada (`app/core/config.py`) e conexão com o banco via
  SQLAlchemy (`app/core/database.py`).
- Models SQLAlchemy das tabelas `usuarios`, `membros`, `treinadores`,
  `especialidades`, `treinos` e `checkins`, mais as tabelas de ligação
  `membros_has_treinos` e `treinadores_has_especialidades`.
- Migrações com Alembic: a primeira migração cria as oito tabelas a partir dos
  models.
- Armazenamento seguro de senhas com hash Argon2 (`app/core/seguranca.py`).
- Cadastro de membro (`POST /auth/cadastro`) em camadas (schema, service e
  rota): validação de entrada, e-mail normalizado, papel fixo `member`, criação
  de usuário e membro em uma única transação. Respostas 201, 409 (e-mail já
  cadastrado) e 422 (dados inválidos).
- Login com token JWT (`POST /auth/login`): confere o hash Argon2, usa mensagem
  única para e-mail inexistente e senha errada e assina o token com uma chave do
  `.env`, com validade de 30 minutos. Respostas 200, 401 e 422.
- Proteção de rotas por token (`app/core/dependencias.py`), com a rota
  `GET /auth/eu` e a autorização por papel (`exigir_papel`), com respostas 401
  (não autenticado) e 403 (sem permissão).
- Evidências dos testes do cadastro na pasta `testes/`.

### Próximos passos
- Aplicar a autorização por papel nas rotas de membros, treinos e check-ins.
- Cadastro e consulta de treinos e check-ins.
- Pipeline de middlewares, tratamento padronizado de erros e logging.
- Cache, load balancing com Docker Compose e mapeamento dos requisitos ASVS.


## [0.1.0] - 2026-11-20 (Parcial 1)

### Adicionado
- Estrutura inicial do projeto em camadas: `app/` com `core`, `middlewares`,
  `models`, `routers`, `schemas` e `services`, além de `migrations/`.
- Ambiente virtual Python e dependências iniciais (FastAPI e Uvicorn),
  registradas em `requirements.txt`.
- API mínima em FastAPI (`app/main.py`) com a rota `GET /saude`, que
  verifica se a aplicação está no ar. A documentação automática fica em `/docs`.
- Modelagem do banco de dados no MySQL Workbench (`academia_api.mwb`), com as
  tabelas `usuarios`, `membros`, `treinadores`, `especialidades`, `treinos`
  e `checkins`, e as tabelas de ligação `membros_has_treinos` e
  `treinadores_has_especialidades`.
- `.gitignore` para manter fora do repositório o ambiente virtual,
  arquivos temporários e variáveis de ambiente.
