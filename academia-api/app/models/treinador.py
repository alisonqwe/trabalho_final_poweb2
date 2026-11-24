# Model da tabela "treinadores": os dados de quem monta os treinos.
# Cada treinador corresponde a exatamente um usuário (a conta de login).

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Treinador(Base):
    __tablename__ = "treinadores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Opcional (nullable=True) e único (unique=True): pode ficar vazio, mas
    # quando preenchido não pode repetir entre treinadores.
    cref: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)

    # Opcional.
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # FK para usuarios, única e obrigatória (ligação 1:1 do diagrama).
    usuarios_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), unique=True, nullable=False
    )