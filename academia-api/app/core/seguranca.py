# Funções de segurança ligadas a senhas.
# Concentrar isso num lugar só facilita trocar o algoritmo no futuro
# e mostrar na apresentação onde a proteção das senhas acontece.

from pwdlib import PasswordHash

# Configuração recomendada pela biblioteca (usa Argon2).
_gerenciador_de_hash = PasswordHash.recommended()


def gerar_hash_da_senha(senha_em_texto: str) -> str:
    # Recebe a senha digitada e devolve o hash que vai para o banco.
    return _gerenciador_de_hash.hash(senha_em_texto)


def verificar_senha(senha_em_texto: str, hash_guardado: str) -> bool:
    # Refaz o embaralhamento da senha digitada e compara com o hash do banco.
    return _gerenciador_de_hash.verify(senha_em_texto, hash_guardado)