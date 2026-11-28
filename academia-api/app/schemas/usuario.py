# Schemas do usuário: descrevem os dados que ENTRAM e SAEM da API.
# O FastAPI valida automaticamente tudo o que chega.

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class CadastroDeMembro(BaseModel):
    
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=2, max_length=100)

   
    email: EmailStr

    
    senha: str = Field(min_length=8, max_length=128)

   
    telefone: str | None = Field(default=None, max_length=20)
    data_nascimento: date | None = None

    # Validação de negócio: ninguém nasce hoje nem no futuro.
    @field_validator("data_nascimento")
    @classmethod
    def nascimento_deve_estar_no_passado(cls, valor):
            if valor is not None and valor >= date.today():
                raise ValueError("A data de nascimento deve estar no passado.")
            return valor


class UsuarioResposta(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    papel: str                    