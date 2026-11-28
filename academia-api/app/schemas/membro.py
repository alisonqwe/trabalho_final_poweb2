# Schema de resposta dos membros: junta dados do usuário (nome, e-mail)
# com dados do membro (telefone, matrícula). Nunca inclui a senha.

from datetime import date

from pydantic import BaseModel, EmailStr


class MembroResposta(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str | None
    data_nascimento: date | None
    data_matricula: date