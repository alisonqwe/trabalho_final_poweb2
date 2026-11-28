# Configuração dos logs: formato único, com data, nível e origem da mensagem.

import logging
import sys


def configurar_logs():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )