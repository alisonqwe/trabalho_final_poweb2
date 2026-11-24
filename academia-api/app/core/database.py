# Este arquivo cria a ligação entre a aplicação e o banco de dados.

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import configuracoes

# O motor gerencia as conexões. O pool_pre_ping testa a conexão antes de
# usá-la, para não quebrar se o banco tiver reiniciado enquanto a API
# estava no ar.
motor_do_banco = create_engine(configuracoes.url_do_banco, pool_pre_ping=True)

# A fábrica cria uma sessão nova sempre que for chamada.
fabrica_de_sessoes = sessionmaker(
    bind=motor_do_banco,
    autoflush=False,
    autocommit=False,
)


# Classe-mãe de todos os models (as tabelas descritas como classes Python).
class Base(DeclarativeBase):
    pass


def obter_sessao():
    # Esta função será "injetada" nas rotas pelo FastAPI. Ela abre uma
    # sessão, entrega para a rota usar (yield) e, quando a rota termina,
    # o finally garante que a sessão fecha, mesmo se der erro no meio.
    sessao = fabrica_de_sessoes()
    try:
        yield sessao
    finally:
        sessao.close()