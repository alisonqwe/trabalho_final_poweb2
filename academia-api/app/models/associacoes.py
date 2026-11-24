# Tabelas de ligação (muitos para muitos). Cada uma só guarda um par de ids.
# As duas colunas juntas formam a chave primária composta, o que impede
# repetir o mesmo par.

from sqlalchemy import Column, ForeignKey, Table

from app.core.database import Base

# Um membro pode ter vários treinos, e um treino pode ser de vários membros.
membros_has_treinos = Table(
    "membros_has_treinos",
    Base.metadata,
    Column("membros_id", ForeignKey("membros.id"), primary_key=True),
    Column("treinos_id", ForeignKey("treinos.id"), primary_key=True),
)

# Um treinador tem uma ou mais especialidades, e uma especialidade
# pode ser de vários treinadores.
treinadores_has_especialidades = Table(
    "treinadores_has_especialidades",
    Base.metadata,
    Column("treinadores_id", ForeignKey("treinadores.id"), primary_key=True),
    Column("especialidades_id", ForeignKey("especialidades.id"), primary_key=True),
)