# Regras de consulta dos membros.

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.membro import Membro
from app.models.usuario import Usuario
from app.schemas.membro import MembroResposta


class PerfilDeMembroNaoEncontrado(Exception):
    # A rota vai transformá-lo em HTTP 404.
    pass


def _montar_resposta(membro: Membro, usuario: Usuario) -> MembroResposta:
    # Junta as duas tabelas num objeto só. Repare que o senha_hash não entra.
    return MembroResposta(
        id=membro.id,
        nome=usuario.nome,
        email=usuario.email,
        telefone=membro.telefone,
        data_nascimento=membro.data_nascimento,
        data_matricula=membro.data_matricula,
    )


def listar_membros(
    sessao: Session, limite: int, deslocamento: int
) -> list[MembroResposta]:
    # JOIN: para cada membro, traz o usuário dono dele (pela chave estrangeira).
    consulta = (
        select(Membro, Usuario)
        .join(Usuario, Membro.usuarios_id == Usuario.id)
        .order_by(Membro.id)
        .limit(limite)
        .offset(deslocamento)
    )
    return [_montar_resposta(membro, usuario) for membro, usuario in sessao.execute(consulta)]


def buscar_perfil(sessao: Session, usuario: Usuario) -> MembroResposta:
    # O membro é descoberto pelo token, e nunca por um id vindo do cliente.
    membro = sessao.scalar(select(Membro).where(Membro.usuarios_id == usuario.id))
    if membro is None:
        raise PerfilDeMembroNaoEncontrado()
    return _montar_resposta(membro, usuario)