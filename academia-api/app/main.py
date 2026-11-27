# Importamos a classe principal do FastAPI.
from fastapi import FastAPI
from app.routers.auth import roteador_auth
from app.routers.treinos import roteador_treinos

# Criamos a aplicação. Tudo na API vai "pendurar" neste objeto.
# O título e a versão aparecem na documentação automática.
aplicacao = FastAPI(
    title="API da Academia",
    version="0.1.0",
)

aplicacao.include_router(roteador_auth)
aplicacao.include_router(roteador_treinos)


# A "etiqueta" @aplicacao.get diz: quando chegar um GET em /saude,
# execute a função logo abaixo.
@aplicacao.get("/saude")
def verificar_saude_da_api():
    # O FastAPI transforma este dicionário Python em JSON sozinho.
    return {"status": "ok"}

