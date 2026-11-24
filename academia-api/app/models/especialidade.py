# Model da tabela "especialidades": lista de áreas de atuação dos treinadores.

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Especialidade(Base):
    __tablename__ = "especialidades"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Único: não pode existir duas vezes a mesma especialidade.
    nome: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)