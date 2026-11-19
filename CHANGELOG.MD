# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.

## [0.1.0] - 2026-11-19 (Parcial 1)

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

### Próximos passos
- Implementar os models e as migrações do banco.
- Autenticação com os papéis member, trainer e admin.
- Cadastro e consulta de membros, treinos e check-ins.