from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TicketCreate(BaseModel):
    descricao: str
    responsavel: str

class TicketRead(BaseModel):
    id: int
    descricao: str
    responsavel: str
    data_atualizacao: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
