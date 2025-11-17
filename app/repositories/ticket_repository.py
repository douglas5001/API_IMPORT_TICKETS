from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.ticket_model import Ticket
from app.schemas.ticket_schema import TicketCreate


class TicketRepository:
    def __init__(self, session: Session):
        self._db = session

    def list_tickets(self) -> list[Ticket]:
        return self._db.query(Ticket).all()

    def get_ticket(self, ticket_id: int) -> Ticket | None:
        return self._db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def create_ticket(self, data: TicketCreate) -> Ticket:
        day = datetime.now(timezone.utc)
        
        ticket = Ticket(
            descricao=data.descricao,
            responsavel=data.responsavel,
            data_atualizacao=day,
        )
        self._db.add(ticket)
        self._db.commit()
        self._db.refresh(ticket)
        return ticket

    def update_ticket(self, ticket_id: int, data: TicketCreate) -> Ticket | None:
        
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return None

        ticket.descricao = data.descricao
        ticket.responsavel = data.responsavel
        ticket.data_atualizacao = datetime.now(timezone.utc)

        self._db.commit()
        self._db.refresh(ticket)
        return ticket

    def delete_ticket(self, ticket_id: int) -> bool:
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False
        self._db.delete(ticket)
        self._db.commit()
        return True
