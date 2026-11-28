# Regras de negócio dos check-ins (frequência dos membros).

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.checkin import Checkin
from app.models.membro import Membro
from app.models.usuario import Usuario


class UsuarioNaoEhMembro(Exception):
    # A rota vai transformá-lo em HTTP 403.
    pass


class CheckinJaRegistradoHoje(Exception):
    # A rota vai transformá-lo em HTTP 409 (conflito).
    pass


def _buscar_membro_do_usuario(sessao: Session, usuario: Usuario) -> Membro:
    # Descobre qual membro é este usuário (a linha dele em "membros").
    membro = sessao.scalar(select(Membro).where(Membro.usuarios_id == usuario.id))
    if membro is None:
        raise UsuarioNaoEhMembro()
    return membro


def registrar_checkin(sessao: Session, usuario: Usuario) -> Checkin:
    membro = _buscar_membro_do_usuario(sessao, usuario)

    # Regra: só um check-in por dia. func.date e func.curdate são do próprio
    # banco, então as duas datas usam o mesmo relógio (o do MySQL).
    checkin_de_hoje = sessao.scalar(
        select(Checkin).where(
            Checkin.membros_id == membro.id,
            func.date(Checkin.data_hora) == func.curdate(),
        )
    )
    if checkin_de_hoje is not None:
        raise CheckinJaRegistradoHoje()

    # A data e a hora são preenchidas pelo banco (server_default).
    novo_checkin = Checkin(membros_id=membro.id)
    sessao.add(novo_checkin)
    sessao.commit()
    sessao.refresh(novo_checkin)
    return novo_checkin


def listar_do_membro(
    sessao: Session, usuario: Usuario, limite: int, deslocamento: int
) -> list[Checkin]:
    membro = _buscar_membro_do_usuario(sessao, usuario)
    consulta = (
        select(Checkin)
        .where(Checkin.membros_id == membro.id)
        .order_by(Checkin.data_hora.desc(), Checkin.id.desc())  # mais recentes primeiro
        .limit(limite)
        .offset(deslocamento)
    )
    return list(sessao.scalars(consulta))


def listar_todos(
    sessao: Session, membro_id: int | None, limite: int, deslocamento: int
) -> list[Checkin]:
    consulta = select(Checkin).order_by(Checkin.data_hora.desc(), Checkin.id.desc())

    # Filtro opcional: só os check-ins de um membro.
    if membro_id is not None:
        consulta = consulta.where(Checkin.membros_id == membro_id)

    return list(sessao.scalars(consulta.limit(limite).offset(deslocamento)))