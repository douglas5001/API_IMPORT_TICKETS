from sqlalchemy.orm import Session
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket_schema import TicketCreate
from app.models.ticket_model import Ticket


class TicketService:
    def __init__(self, session: Session):
        self._repo = TicketRepository(session)

    def list_tickets(self) -> list[Ticket]:
        return self._repo.list_tickets()

    def get_ticket(self, ticket_id: int) -> Ticket | None:
        return self._repo.get_ticket(ticket_id)

    def create_ticket(self, data: TicketCreate) -> Ticket:
        return self._repo.create_ticket(data)

    def update_ticket(self, ticket_id: int, data: TicketCreate) -> Ticket | None:
        return self._repo.update_ticket(ticket_id, data)

    def delete_ticket(self, ticket_id: int) -> bool:
        return self._repo.delete_ticket(ticket_id)
