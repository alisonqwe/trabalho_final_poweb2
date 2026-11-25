# Model da tabela "membros": os dados de quem frequenta a academia.
# Cada membro corresponde a exatamente um usuário (a conta de login).

from datetime import date  # tipo "data" do Python (sem hora)

from sqlalchemy import Date, ForeignKey, String  # Date e ForeignKey são novos
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Membro(Base):
    __tablename__ = "membros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

   
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    
    data_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)


    data_matricula: Mapped[date] = mapped_column(Date, nullable=False)

    # Chave estrangeira: aponta para a tabela usuarios. O banco só aceita
    # um número que exista em usuarios.id. O unique=True garante que um
    # usuário não tenha dois registros de membro (a ligação 1:1 do diagrama).
    usuarios_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), unique=True, nullable=False
    )