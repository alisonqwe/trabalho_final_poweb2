# trabalho_final_poweb2
 
# API da Academia

API RESTful para gestão de uma academia de ginástica (membros, treinos e
check-ins), desenvolvida para o Trabalho Final de Programação para a Web II
(UFPI, CSHNB, Bacharelado em Sistemas de Informação).

**Stack:** Python, FastAPI e Uvicorn. Banco de dados e demais componentes
serão documentados conforme forem implementados.

## Como executar localmente

Pré-requisitos: Python 3, Docker e Docker Compose.

```bash
# 1. Entrar na pasta da API
cd academia-api

# 2. Criar o arquivo de configuração a partir do modelo
cp .env.example .env
```

Abra o `.env` e troque os valores `troque_...` por senhas e por uma chave
secreta de sua escolha (nunca versione esse arquivo). Para gerar uma chave
aleatória: `python -c "import secrets; print(secrets.token_urlsafe(48))"`.

```bash
# 3. Subir o banco de dados (MySQL em container, porta 3307 do computador)
docker compose up -d

# 4. Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\Activate.ps1     # Windows (PowerShell)

# 5. Instalar as dependências
pip install -r requirements.txt

# 6. Criar as tabelas (migrações do Alembic)
alembic upgrade head

# 7. Subir a API
uvicorn app.main:aplicacao --reload
```

Com o servidor no ar:

- Verificação de saúde: http://127.0.0.1:8000/saude
- Documentação interativa: http://127.0.0.1:8000/docs

Para desligar o banco: `docker compose down` (os dados são mantidos no
volume; use `docker compose down -v` para apagá-los também).

## Estrutura do projeto

```
academia-api/
├── app/
│   ├── main.py          # ponto de entrada da API
│   ├── routers/         # rotas (endpoints)
│   ├── models/          # tabelas do banco
│   ├── schemas/         # formato dos dados de entrada e saída
│   ├── services/        # regras de negócio
│   ├── middlewares/     # pipeline de middlewares
│   └── core/            # configurações, segurança e cache
├── migrations/          # versionamento do esquema do banco
└── docker-compose.yml   # execução com múltiplas instâncias
```

O diagrama do banco de dados está em `academia_api.mwb` (MySQL Workbench).

## Status

Parcial 2: banco de dados com migrações, hash seguro de senhas e cadastro de membro.
Veja o histórico completo em [CHANGELOG.MD](CHANGELOG.MD).