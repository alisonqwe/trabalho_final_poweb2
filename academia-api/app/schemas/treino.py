# Schemas dos treinos: o que entra e o que sai da API.

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class NovoTreino(BaseModel):
    # Remove espaços sobrando no começo e no fim dos textos.
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=2, max_length=100)
    descricao: str | None = Field(default=None, max_length=5000)

    # Literal: só estes três valores são aceitos. Outro valor vira erro 422.
    nivel: Literal["iniciante", "intermediario", "avancado"]

    # Opcional. Entre 1 minuto e 10 horas.
    duracao_minutos: int | None = Field(default=None, ge=1, le=600)

    # Não existe "treinadores_id" aqui: o treinador vem do token, não do cliente.


class TreinoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str | None
    nivel: str
    duracao_minutos: int | None
    criado_em: datetime
    treinadores_id: int