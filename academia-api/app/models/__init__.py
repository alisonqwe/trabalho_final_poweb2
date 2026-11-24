# Importa todos os models num lugar só, para que o Alembic os encontre.

from app.models.associacoes import (  # noqa: F401
    membros_has_treinos,
    treinadores_has_especialidades,
)
from app.models.checkin import Checkin  # noqa: F401
from app.models.especialidade import Especialidade  # noqa: F401
from app.models.membro import Membro  # noqa: F401
from app.models.treinador import Treinador  # noqa: F401
from app.models.treino import Treino  # noqa: F401
from app.models.usuario import Usuario  # noqa: F401