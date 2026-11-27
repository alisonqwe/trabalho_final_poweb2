
# Como usar (com o .venv ativo e dentro de academia-api/):
#   python criar_usuario_interno.py

from getpass import getpass

from sqlalchemy import select

from app.core.database import fabrica_de_sessoes
from app.core.seguranca import gerar_hash_da_senha
from app.models.treinador import Treinador
from app.models.usuario import Usuario

PAPEIS_PERMITIDOS = ("admin", "trainer")


def criar_usuario_interno():
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()
    papel = input("Papel (admin ou trainer): ").strip()
    # getpass não mostra o que é digitado e não deixa a senha no histórico.
    senha = getpass("Senha (mínimo 8 caracteres): ")

    if papel not in PAPEIS_PERMITIDOS:
        print("Papel inválido. Use admin ou trainer.")
    elif len(senha) < 8 or not nome or not email:
        print("Dados inválidos. Preencha tudo e use senha com 8+ caracteres.")
    else:
        sessao = fabrica_de_sessoes()
        ja_existe = sessao.scalar(select(Usuario).where(Usuario.email == email))

        if ja_existe is not None:
            print("Já existe um usuário com esse e-mail.")
        else:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha_hash=gerar_hash_da_senha(senha),
                papel=papel,
            )
            sessao.add(novo_usuario)
            # flush: o banco gera o id do usuário, que o treinador precisa.
            sessao.flush()

            # Treinador tem uma linha extra na tabela "treinadores".
            if papel == "trainer":
                sessao.add(Treinador(usuarios_id=novo_usuario.id))

            sessao.commit()
            print(f"Usuário {papel} criado com sucesso (id {novo_usuario.id}).")

        sessao.close()


if __name__ == "__main__":
    criar_usuario_interno()