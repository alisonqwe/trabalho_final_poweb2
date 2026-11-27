# Funções de segurança ligadas a senhas.
# Concentrar isso num lugar só facilita trocar o algoritmo no futuro
# e mostrar na apresentação onde a proteção das senhas acontece.
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import configuracoes
from pwdlib import PasswordHash

# Configuração recomendada pela biblioteca (usa Argon2).
_gerenciador_de_hash = PasswordHash.recommended()


def gerar_hash_da_senha(senha_em_texto: str) -> str:
    # Recebe a senha digitada e devolve o hash que vai para o banco.
    return _gerenciador_de_hash.hash(senha_em_texto)


def verificar_senha(senha_em_texto: str, hash_guardado: str) -> bool:
    # Refaz o embaralhamento da senha digitada e compara com o hash do banco.
    return _gerenciador_de_hash.verify(senha_em_texto, hash_guardado)


class TokenInvalido(Exception):
    # Erro único para qualquer problema com o token (adulterado, vencido,
    # malformado). Quem chamar só precisa tratar este caso.
    pass


def criar_token_de_acesso(usuario_id: int, papel: str) -> str:
    # Calcula o momento em que o token deixa de valer (agora + 30 minutos).
    # Usamos UTC para não depender do fuso horário do servidor.
    momento_de_expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=configuracoes.EXPIRACAO_DO_TOKEN_MINUTOS
    )

    conteudo_do_token = {
        "sub": str(usuario_id),  # quem é o usuário
        "papel": papel,          # o que ele pode fazer
        "exp": momento_de_expiracao,  # até quando vale
    }

    # Assina o conteúdo com a chave secreta e devolve o texto do token.
    return jwt.encode(
        conteudo_do_token,
        configuracoes.CHAVE_SECRETA_JWT,
        algorithm=configuracoes.ALGORITMO_JWT,
    )


def ler_token_de_acesso(token: str) -> dict:
    try:
        # Confere a assinatura e o prazo. Dois cuidados de segurança:
        # - "algorithms" é uma lista fixa: o token não escolhe como será
        #   conferido (evita ataques que trocam o algoritmo).
        # - "require" exige que o token tenha "exp" e "sub".
        return jwt.decode(
            token,
            configuracoes.CHAVE_SECRETA_JWT,
            algorithms=[configuracoes.ALGORITMO_JWT],
            options={"require": ["exp", "sub"]},
        )
    except jwt.PyJWTError:
        # Qualquer falha da biblioteca vira o nosso erro simples.
        raise TokenInvalido()