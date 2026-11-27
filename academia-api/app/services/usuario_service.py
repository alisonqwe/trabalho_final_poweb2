# Regras de negócio do usuário. A rota só chama estas funções;
# quem decide o que pode ou não acontecer é este arquivo.

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.seguranca import (
    criar_token_de_acesso,
    gerar_hash_da_senha,
    verificar_senha,
)
from app.schemas.auth import LoginEntrada
from app.models.membro import Membro
from app.models.usuario import Usuario
from app.schemas.usuario import CadastroDeMembro


class EmailJaCadastrado(Exception):
    # Erro de negócio: a rota vai transformá-lo em HTTP 409 (conflito).
    pass


def cadastrar_membro(sessao: Session, dados: CadastroDeMembro) -> Usuario:
    # Guardamos o e-mail em minúsculas para "Ana@x.com" e "ana@x.com"
    # não virarem duas contas diferentes.
    email_normalizado = dados.email.lower()

    # Consulta parametrizada (feita pelo SQLAlchemy): protege contra injeção de SQL.
    usuario_existente = sessao.scalar(
        select(Usuario).where(Usuario.email == email_normalizado)
    )
    if usuario_existente is not None:
        raise EmailJaCadastrado()

    # O papel é fixo aqui, e não vem do cliente: o cadastro público só cria membros.
    novo_usuario = Usuario(
        nome=dados.nome,
        email=email_normalizado,
        senha_hash=gerar_hash_da_senha(dados.senha),
        papel="member",
    )
    sessao.add(novo_usuario)

    # flush: envia o INSERT para o banco gerar o id, mas ainda sem finalizar.
    sessao.flush()

    novo_membro = Membro(
        telefone=dados.telefone,
        data_nascimento=dados.data_nascimento,
        data_matricula=date.today(),
        usuarios_id=novo_usuario.id,
    )
    sessao.add(novo_membro)

    # commit: grava usuário e membro juntos. Se algo falhar antes daqui,
    # nada fica salvo.
    sessao.commit()
    sessao.refresh(novo_usuario)

    return novo_usuario



class CredenciaisInvalidas(Exception):
    # Erro de negócio: a rota vai transformá-lo em HTTP 401.
    pass


# Hash de uma senha qualquer, calculado uma vez só. Serve para gastar o mesmo
# tempo de conferência quando o e-mail não existe (ver fazer_login).
_HASH_FALSO = gerar_hash_da_senha("senha-que-ninguem-usa")


def fazer_login(sessao: Session, dados: LoginEntrada) -> str:
    usuario = sessao.scalar(
        select(Usuario).where(Usuario.email == dados.email.lower())
    )

    # Se o usuário não existe, conferimos a senha contra o hash falso, só para
    # a resposta demorar o mesmo tempo que demoraria com um usuário real.
    hash_para_conferir = usuario.senha_hash if usuario else _HASH_FALSO
    senha_confere = verificar_senha(dados.senha, hash_para_conferir)

    # Um único erro para os dois casos (e-mail inexistente ou senha errada).
    if usuario is None or not senha_confere:
        raise CredenciaisInvalidas()

    return criar_token_de_acesso(usuario.id, usuario.papel)