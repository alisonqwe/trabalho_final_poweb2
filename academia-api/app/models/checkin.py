# Model da tabela "checkins": cada vez que um membro registra presença.

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Checkin(Base):
    __tablename__ = "checkins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Data e hora da presença, preenchidas pelo banco.
    data_hora: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    # FK: o membro que fez o check-in. Sem unique, porque um membro tem
    # vários check-ins (ligação 1:n do diagrama).
    membros_id: Mapped[int] = mapped_column(
        ForeignKey("membros.id"), nullable=False
    )