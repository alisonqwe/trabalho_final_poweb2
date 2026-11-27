# Schemas do login: o que entra (e-mail e senha) e o que sai (o token).

from pydantic import BaseModel, EmailStr, Field


class LoginEntrada(BaseModel):
    email: EmailStr
    # Só limitamos o máximo, para não aceitar senhas gigantes. O mínimo
    # não é cobrado aqui: no login, quem erra só recebe "inválido".
    senha: str = Field(max_length=128)


class TokenResposta(BaseModel):
    access_token: str
    # "bearer" diz ao cliente como enviar o token: "Authorization: Bearer <token>".
    token_type: str = "bearer"