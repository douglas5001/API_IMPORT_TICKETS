from sqlalchemy.orm import Session
from app.repositories.ticket.ticket_repository import TicketRepository
from app.schemas.ticket import ticket_schema
from app.models.ticket.ticket_model import Ticket


class TicketService:
    def __init__(self, session: Session):
        self._repo = TicketRepository(session)

    def list_tickets(self) -> list[Ticket]:
        return self._repo.list_tickets()

    def get_ticket(self, ticket_id: int) -> Ticket | None:
        return self._repo.get_ticket(ticket_id)

    def create_ticket(self, data: ticket_schema.TicketCreate) -> Ticket:
        return self._repo.create_ticket(data)

    def update_ticket(self, ticket_id: int, data: ticket_schema.TicketCreate) -> Ticket | None:
        return self._repo.update_ticket(ticket_id, data)

    def delete_ticket(self, ticket_id: int) -> bool:
        return self._repo.delete_ticket(ticket_id)

    def import_tickets(self, rows: list[ticket_schema.TicketImportRow]) -> dict:
        created = 0
        updated = 0
        skipped = 0

        for row in rows:
            _, action = self._repo.upsert_from_import(row)
            if action == "created":
                created += 1
            elif action == "updated":
                updated += 1
            else:
                skipped += 1

        return {
            "total": len(rows),
            "created": created,
            "updated": updated,
            "skipped": skipped,
        }