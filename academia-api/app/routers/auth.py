# Rotas de autenticação. Por enquanto só o cadastro; o login vem depois.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.schemas.usuario import CadastroDeMembro, UsuarioResposta
from app.services import usuario_service

# prefix: todas as rotas daqui começam com /auth.
# tags: agrupa as rotas na documentação (/docs).
roteador_auth = APIRouter(prefix="/auth", tags=["Autenticação"])


@roteador_auth.post(
    "/cadastro",
    response_model=UsuarioResposta,  # filtra a resposta: só id, nome, email e papel
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_membro(
    dados: CadastroDeMembro,  # o FastAPI valida o corpo com o schema
    sessao: Session = Depends(obter_sessao),  # sessão do banco, entregue pelo FastAPI
):
    try:
        usuario_criado = usuario_service.cadastrar_membro(sessao, dados)
    except usuario_service.EmailJaCadastrado:
        # Traduz o erro de negócio em erro HTTP.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )

    return usuario_criado