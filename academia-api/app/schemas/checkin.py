# Schema dos check-ins. Não existe schema de entrada: o pedido não leva
# nenhum dado, porque o membro e a hora vêm do token e do banco.

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckinResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_hora: datetime
    membros_id: int