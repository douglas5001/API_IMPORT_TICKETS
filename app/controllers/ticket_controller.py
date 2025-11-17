from collections.abc import Generator
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import SessionLocal, get_db
from app.schemas.ticket_schema import TicketCreate, TicketRead
from app.services.ticket_service import TicketService

router = APIRouter()



def get_ticket_service(db: Session = Depends(get_db)) -> TicketService:
    return TicketService(session=db)


@router.get("/tickets", response_model=list[TicketRead])
def get_tickets(service: TicketService = Depends(get_ticket_service)):
    return service.list_tickets()


@router.post("/tickets", response_model=TicketRead)
def create_ticket(
    ticket: TicketCreate,
    service: TicketService = Depends(get_ticket_service),
):
    return service.create_ticket(ticket)


@router.get("/tickets/{ticket_id}", response_model=TicketRead)
def get_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service),
):
    obj = service.get_ticket(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return obj


@router.put("/tickets/{ticket_id}", response_model=TicketRead)
def update_ticket(
    ticket_id: int,
    ticket: TicketCreate,
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
