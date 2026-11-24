# Model da tabela "treinos": os treinos montados pelos treinadores.

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Treino(Base):
    __tablename__ = "treinos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    # Opcional. MEDIUMTEXT é o texto longo, como no diagrama.
    descricao: Mapped[str | None] = mapped_column(MEDIUMTEXT, nullable=True)

    # "iniciante", "intermediario" ou "avancado" (validado na API).
    nivel: Mapped[str] = mapped_column(String(20), nullable=False)

    # Opcional.
    duracao_minutos: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Preenchido pelo próprio banco no momento do cadastro.
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    # FK: o treinador que criou o treino (ligação 1:n do diagrama).
    treinadores_id: Mapped[int] = mapped_column(
        ForeignKey("treinadores.id"), nullable=False
    )