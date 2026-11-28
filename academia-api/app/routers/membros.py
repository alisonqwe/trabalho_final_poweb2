# Rotas de consulta de membros.

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.core.dependencias import exigir_papel
from app.models.usuario import Usuario
from app.schemas.membro import MembroResposta
from app.services import membro_service

roteador_membros = APIRouter(prefix="/membros", tags=["Membros"])


@roteador_membros.get(
    "",
    response_model=list[MembroResposta],
    # Só quem trabalha na academia vê os dados de todos os membros.
    dependencies=[Depends(exigir_papel("trainer", "admin"))],
)
def listar_membros(
    limite: int = Query(default=20, ge=1, le=100),
    deslocamento: int = Query(default=0, ge=0),
    sessao: Session = Depends(obter_sessao),
):
    return membro_service.listar_membros(sessao, limite, deslocamento)


@roteador_membros.get("/eu", response_model=MembroResposta)
def ver_meu_perfil(
    # Só membro tem perfil de membro, e é sempre o dele (vem do token).
    usuario: Usuario = Depends(exigir_papel("member")),
    sessao: Session = Depends(obter_sessao),
):
    try:
        return membro_service.buscar_perfil(sessao, usuario)
    except membro_service.PerfilDeMembroNaoEncontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de membro não encontrado.",
        )