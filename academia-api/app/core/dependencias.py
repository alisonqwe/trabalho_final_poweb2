# Dependências: funções que o FastAPI roda ANTES das rotas protegidas.

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.core.seguranca import TokenInvalido, ler_token_de_acesso
from app.models.usuario import Usuario

# Lê o cabeçalho "Authorization: Bearer <token>". Também faz aparecer o
# botão "Authorize" (cadeado) no /docs. Com auto_error=False, o 401 é nosso.
esquema_bearer = HTTPBearer(auto_error=False)


def _erro_nao_autenticado() -> HTTPException:
    # Mensagem única para todos os motivos: não dizemos se o token estava
    # vencido, adulterado ou se o usuário sumiu.
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def usuario_logado(
    credenciais: HTTPAuthorizationCredentials | None = Depends(esquema_bearer),
    sessao: Session = Depends(obter_sessao),
) -> Usuario:
    # 1. Veio token?
    if credenciais is None:
        raise _erro_nao_autenticado()

    # 2. A assinatura e o prazo valem?
    try:
        conteudo = ler_token_de_acesso(credenciais.credentials)
        usuario_id = int(conteudo["sub"])
    except (TokenInvalido, ValueError):
        raise _erro_nao_autenticado()

    # 3. O usuário do token ainda existe?
    usuario = sessao.get(Usuario, usuario_id)
    if usuario is None:
        raise _erro_nao_autenticado()

    return usuario

def exigir_papel(*papeis_permitidos: str):
    # Fábrica: recebe os papéis permitidos e devolve a dependência pronta.
    # Uso numa rota:  Depends(exigir_papel("admin", "trainer"))

    def verificar(usuario: Usuario = Depends(usuario_logado)) -> Usuario:
        # Chegou aqui, então o token é válido (senão já teria dado 401).
        if usuario.papel not in papeis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para esta ação.",
            )
        return usuario

    return verificar