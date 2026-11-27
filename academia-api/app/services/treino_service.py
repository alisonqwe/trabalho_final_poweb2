# Regras de negócio dos treinos.

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.treinador import Treinador
from app.models.treino import Treino
from app.models.usuario import Usuario
from app.schemas.treino import NovoTreino


class UsuarioNaoEhTreinador(Exception):
    # A rota vai transformá-lo em HTTP 403.
    pass


def criar_treino(sessao: Session, usuario: Usuario, dados: NovoTreino) -> Treino:
    # Descobre qual treinador é este usuário (a linha dele em "treinadores").
    treinador = sessao.scalar(
        select(Treinador).where(Treinador.usuarios_id == usuario.id)
    )
    if treinador is None:
        raise UsuarioNaoEhTreinador()

    novo_treino = Treino(
        nome=dados.nome,
        descricao=dados.descricao,
        nivel=dados.nivel,
        duracao_minutos=dados.duracao_minutos,
        treinadores_id=treinador.id,  # vem do token, nunca do cliente
    )
    sessao.add(novo_treino)
    sessao.commit()
    sessao.refresh(novo_treino)
    return novo_treino


def listar_treinos(
    sessao: Session, nivel: str | None, limite: int, deslocamento: int
) -> list[Treino]:
    consulta = select(Treino).order_by(Treino.id)

    # Filtro opcional por nível.
    if nivel is not None:
        consulta = consulta.where(Treino.nivel == nivel)

    # Paginação: "limite" é quantos vêm, "deslocamento" é quantos pular.
    consulta = consulta.limit(limite).offset(deslocamento)
    return list(sessao.scalars(consulta))


def buscar_treino(sessao: Session, treino_id: int) -> Treino | None:
    # Devolve None se o treino não existir (a rota transforma em 404).
    return sessao.get(Treino, treino_id)