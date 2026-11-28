# Tratamento de erros: toda resposta de erro da API segue o mesmo formato.
# Detalhes internos (traceback, caminhos, valores enviados) NUNCA vão ao cliente.

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as ErroHTTP

registro = logging.getLogger("academia.erros")


def _resposta_de_erro(codigo, mensagem, campos=None, cabecalhos=None):
    # Monta o corpo padrão. "campos" só existe nos erros de validação.
    corpo = {"erro": {"codigo": codigo, "mensagem": mensagem}}
    if campos:
        corpo["erro"]["campos"] = campos
    return JSONResponse(status_code=codigo, content=corpo, headers=cabecalhos)


async def tratar_erro_http(requisicao: Request, erro: ErroHTTP):
    # Pega os erros que nós levantamos (401, 403, 404, 409) e também os do
    # framework (rota que não existe, método não permitido).
    return _resposta_de_erro(
        erro.status_code, str(erro.detail), cabecalhos=erro.headers
    )


async def tratar_erro_de_validacao(requisicao: Request, erro: RequestValidationError):
    campos = []
    for item in erro.errors():
        # "loc" vem como ("body", "email"): tiramos a parte técnica.
        partes = [str(p) for p in item["loc"] if p not in ("body", "query", "path")]
        # Repare: NÃO copiamos o "input", que é o valor enviado (pode ser senha).
        campos.append({"campo": ".".join(partes) or "corpo", "mensagem": item["msg"]})
    return _resposta_de_erro(422, "Dados inválidos.", campos=campos)


async def tratar_erro_inesperado(requisicao: Request, erro: Exception):
    # Bug que não previmos. O traceback completo vai para o log do servidor.
    registro.exception(
        "Erro inesperado em %s %s", requisicao.method, requisicao.url.path
    )
    # O cliente só recebe uma mensagem genérica.
    return _resposta_de_erro(500, "Erro interno do servidor.")


def registrar_tratadores_de_erro(aplicacao: FastAPI):
    aplicacao.add_exception_handler(ErroHTTP, tratar_erro_http)
    aplicacao.add_exception_handler(RequestValidationError, tratar_erro_de_validacao)
    aplicacao.add_exception_handler(Exception, tratar_erro_inesperado)