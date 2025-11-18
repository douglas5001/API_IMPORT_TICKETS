from collections.abc import Generator
from io import BytesIO
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
import pandas as pd
from sqlalchemy.orm import Session
from app.config.database import SessionLocal, get_db
from app.schemas import ticket_schema
from app.services.ticket_service import TicketService

router = APIRouter()

def get_ticket_service(db: Session = Depends(get_db)) -> TicketService:
    return TicketService(session=db)


@router.get("/tickets", response_model=list[ticket_schema.TicketRead])
def get_tickets(service: TicketService = Depends(get_ticket_service)):
    return service.list_tickets()


@router.post("/tickets", response_model=ticket_schema.TicketRead)
def create_ticket(
    ticket: ticket_schema.TicketCreate,
    service: TicketService = Depends(get_ticket_service),
):
    return service.create_ticket(ticket)


@router.get("/tickets/{ticket_id}", response_model=ticket_schema.TicketRead)
def get_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service),
):
    obj = service.get_ticket(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return obj


@router.put("/tickets/{ticket_id}", response_model=ticket_schema.TicketRead)
def update_ticket(
    ticket_id: int,
    ticket: ticket_schema.TicketCreate,
    service: TicketService = Depends(get_ticket_service),
):
    updated = service.update_ticket(ticket_id, ticket)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated


@router.delete("/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service),
):
    success = service.delete_ticket(ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"success": True}


@router.post("/tickets/import")
def import_tickets(
    file: UploadFile = File(...),
    service: TicketService = Depends(get_ticket_service),
):
    """
    Importa tickets em massa a partir de um arquivo Excel.

    Colunas esperadas: cod_ticket, descricao, responsavel, data_atualizacao
    """
    content = file.file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Arquivo vazio")

    try:
        df = pd.read_excel(BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler Excel: {e}")

    expected_cols = {"cod_ticket", "descricao", "responsavel", "data_atualizacao"}
    if not expected_cols.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"Excel deve conter as colunas: {', '.join(sorted(expected_cols))}",
        )

    # Tive que coverter, estava com bug de 3 h no banco
    df["data_atualizacao"] = pd.to_datetime(
        df["data_atualizacao"],
        errors="coerce",
        dayfirst=True,
    )
    LOCAL_TZ = ZoneInfo("America/Sao_Paulo")
    df["data_atualizacao"] = df["data_atualizacao"].dt.tz_localize(LOCAL_TZ)

    rows: list[ticket_schema.TicketImportRow] = []
    for record in df.to_dict(orient="records"):
        dt = record["data_atualizacao"]
        if pd.isna(dt):
            dt = None

        row = ticket_schema.TicketImportRow(
            cod_ticket=str(record["cod_ticket"]),
            descricao=str(record["descricao"]),
            responsavel=str(record["responsavel"]),
            data_atualizacao=dt,
        )
        rows.append(row)

    result = service.import_tickets(rows)
    return result