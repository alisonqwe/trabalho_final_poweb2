# Regras de negócio do usuário. A rota só chama estas funções;
# quem decide o que pode ou não acontecer é este arquivo.

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.seguranca import gerar_hash_da_senha
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