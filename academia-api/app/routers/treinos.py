# Rotas de treinos.

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.core.dependencias import exigir_papel, usuario_logado
from app.models.usuario import Usuario
from app.schemas.treino import NovoTreino, TreinoResposta
from app.services import treino_service

roteador_treinos = APIRouter(prefix="/treinos", tags=["Treinos"])


@roteador_treinos.post(
    "", response_model=TreinoResposta, status_code=status.HTTP_201_CREATED
)
def criar_treino(
    dados: NovoTreino,
    # Só treinador entra aqui: admin e membro recebem 403.
    usuario: Usuario = Depends(exigir_papel("trainer")),
    sessao: Session = Depends(obter_sessao),
):
    try:
        return treino_service.criar_treino(sessao, usuario, dados)
    except treino_service.UsuarioNaoEhTreinador:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para esta ação.",
        )


@roteador_treinos.get(
    "",
    response_model=list[TreinoResposta],
    dependencies=[Depends(usuario_logado)],  # exige login, sem usar o usuário
)
def listar_treinos(
    nivel: Literal["iniciante", "intermediario", "avancado"] | None = None,
    # Query(...) valida: entre 1 e 100 itens por página, e deslocamento >= 0.
    limite: int = Query(default=20, ge=1, le=100),
    deslocamento: int = Query(default=0, ge=0),
    sessao: Session = Depends(obter_sessao),
):
    return treino_service.listar_treinos(sessao, nivel, limite, deslocamento)


@roteador_treinos.get(
    "/{treino_id}",
    response_model=TreinoResposta,
    dependencies=[Depends(usuario_logado)],
)
def buscar_treino(treino_id: int, sessao: Session = Depends(obter_sessao)):
    treino = treino_service.buscar_treino(sessao, treino_id)
    if treino is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treino não encontrado.",
        )
    return treino