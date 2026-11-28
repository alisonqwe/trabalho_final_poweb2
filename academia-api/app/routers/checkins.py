# Rotas de check-ins (frequência dos membros).

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.core.dependencias import exigir_papel
from app.models.usuario import Usuario
from app.schemas.checkin import CheckinResposta
from app.services import checkin_service

roteador_checkins = APIRouter(prefix="/checkins", tags=["Check-ins"])


@roteador_checkins.post(
    "", response_model=CheckinResposta, status_code=status.HTTP_201_CREATED
)
def registrar_checkin(
    # Só membro registra presença, e sempre a própria (o membro vem do token).
    usuario: Usuario = Depends(exigir_papel("member")),
    sessao: Session = Depends(obter_sessao),
):
    try:
        return checkin_service.registrar_checkin(sessao, usuario)
    except checkin_service.UsuarioNaoEhMembro:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para esta ação.",
        )
    except checkin_service.CheckinJaRegistradoHoje:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Check-in de hoje já registrado.",
        )


@roteador_checkins.get("/meus", response_model=list[CheckinResposta])
def listar_meus_checkins(
    limite: int = Query(default=20, ge=1, le=100),
    deslocamento: int = Query(default=0, ge=0),
    usuario: Usuario = Depends(exigir_papel("member")),
    sessao: Session = Depends(obter_sessao),
):
    try:
        return checkin_service.listar_do_membro(sessao, usuario, limite, deslocamento)
    except checkin_service.UsuarioNaoEhMembro:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para esta ação.",
        )


@roteador_checkins.get(
    "",
    response_model=list[CheckinResposta],
    # Treinador e admin consultam a frequência de todos os membros.
    dependencies=[Depends(exigir_papel("trainer", "admin"))],
)
def listar_todos_os_checkins(
    membro_id: int | None = None,  # filtro opcional por membro
    limite: int = Query(default=20, ge=1, le=100),
    deslocamento: int = Query(default=0, ge=0),
    sessao: Session = Depends(obter_sessao),
):
    return checkin_service.listar_todos(sessao, membro_id, limite, deslocamento)