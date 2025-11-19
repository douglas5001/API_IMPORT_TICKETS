from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TicketCreate(BaseModel):
    cod_ticket: str
    descricao: str
    responsavel: str
    # data_atualizacao: datetime


class TicketRead(BaseModel):
    id: int
    cod_ticket: str
    descricao: str
    responsavel: str
    data_atualizacao: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketImportRow(BaseModel):
    cod_ticket: str
    descricao: str
    responsavel: str
    data_atualizacao: datetime | None = None
