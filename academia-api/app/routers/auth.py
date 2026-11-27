# Rotas de autenticação. Por enquanto só o cadastro; o login vem depois.
from app.core.dependencias import usuario_logado
from app.models.usuario import Usuario

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginEntrada, TokenResposta

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

@roteador_auth.post("/login", response_model=TokenResposta)
def entrar(
    dados: LoginEntrada,  # validado pelo schema (e-mail com formato certo)
    sessao: Session = Depends(obter_sessao),
):
    try:
        token = usuario_service.fazer_login(sessao, dados)
    except usuario_service.CredenciaisInvalidas:
        # Mensagem única para e-mail inexistente e senha errada.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # access_token e token_type são nomes exigidos pelo padrão OAuth2,
    # por isso ficam em inglês no JSON de resposta.
    return TokenResposta(access_token=token)

@roteador_auth.get("/eu", response_model=UsuarioResposta)
def quem_sou_eu(usuario: Usuario = Depends(usuario_logado)):
    # Só chega aqui quem mandou um token válido. A resposta é do próprio
    # usuário do token, nunca de outra pessoa.
    return usuario