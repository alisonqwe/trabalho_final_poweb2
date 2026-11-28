# Middleware de logging: registra um resumo de cada requisição.
# NUNCA grava o corpo do pedido nem o cabeçalho Authorization.

import logging
import time
import uuid

from fastapi import Request

registro = logging.getLogger("academia.requisicoes")


async def registrar_requisicao(requisicao: Request, proxima):
    # ID curto para achar este pedido nos logs (e para o cliente reportar).
    id_da_requisicao = uuid.uuid4().hex[:12]
    inicio = time.perf_counter()
    ip = requisicao.client.host if requisicao.client else "desconhecido"

    try:
        resposta = await proxima(requisicao)
    except Exception:
        # Erro inesperado: registramos e deixamos o tratador de erros responder.
        registro.error(
            "id=%s %s %s -> erro inesperado ip=%s",
            id_da_requisicao, requisicao.method, requisicao.url.path, ip,
        )
        raise

    duracao_ms = (time.perf_counter() - inicio) * 1000
    # url.path não inclui a query string (que poderia ter dados sensíveis).
    registro.info(
        "id=%s %s %s -> %s (%.0f ms) ip=%s",
        id_da_requisicao, requisicao.method, requisicao.url.path,
        resposta.status_code, duracao_ms, ip,
    )
    resposta.headers["X-Request-ID"] = id_da_requisicao
    return resposta