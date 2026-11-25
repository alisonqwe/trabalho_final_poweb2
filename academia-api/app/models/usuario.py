# Model da tabela "usuarios": quem faz login na API (membro, treinador ou admin).

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    nome: Mapped[str] = mapped_column(String(100), nullable=False)

   
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    
    papel: Mapped[str] = mapped_column(String(20), nullable=False)

    # server_default=func.now(): quem preenche a data é o próprio banco,
    # no momento do cadastro. É o "padrão CURRENT_TIMESTAMP" do diagrama.
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )