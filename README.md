# trabalho_final_poweb2
 
# API da Academia

API RESTful para gestão de uma academia de ginástica (membros, treinos e
check-ins), desenvolvida para o Trabalho Final de Programação para a Web II
(UFPI, CSHNB, Bacharelado em Sistemas de Informação).

**Stack:** Python, FastAPI e Uvicorn. Banco de dados e demais componentes
serão documentados conforme forem implementados.

## Como executar localmente

Pré-requisito: Python 3 instalado.

```bash
# 1. Entrar na pasta da API
cd academia-api

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\Activate.ps1     # Windows (PowerShell)

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Subir o servidor
uvicorn app.main:aplicacao --reload
```

Com o servidor no ar:

- Verificação de saúde: http://127.0.0.1:8000/saude
- Documentação interativa: http://127.0.0.1:8000/docs

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

Parcial 1: estrutura do projeto, rota `/saude` e modelagem do banco.
Veja o histórico completo em [CHANGELOG.MD](CHANGELOG.MD).