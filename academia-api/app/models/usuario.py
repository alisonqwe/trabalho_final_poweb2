# Model da tabela "usuarios": quem faz login na API (membro, treinador ou admin).

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Usuario(Base):
    # Nome da tabela no banco (plural, como no diagrama).
    __tablename__ = "usuarios"

    # primary_key: identifica cada linha. O banco gera o número sozinho
    # (autoincrement), o mesmo AI que marcamos no Workbench.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    # unique=True: o banco recusa dois usuários com o mesmo e-mail.
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    # Aqui fica o hash da senha, nunca a senha em si.
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # "member", "trainer" ou "admin". Os valores aceitos serão validados
    # na API (schemas), igual fizemos com o status na Engenharia 2.
    papel: Mapped[str] = mapped_column(String(20), nullable=False)

    # server_default=func.now(): quem preenche a data é o próprio banco,
    # no momento do cadastro. É o "padrão CURRENT_TIMESTAMP" do diagrama.
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )