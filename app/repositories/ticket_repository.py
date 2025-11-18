from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from app.models.ticket_model import Ticket
from app.schemas import ticket_schema

LOCAL_TZ = ZoneInfo("America/Sao_Paulo")

class TicketRepository:
    def __init__(self, session: Session):
        self._db = session

    def list_tickets(self) -> list[Ticket]:
        return self._db.query(Ticket).all()

    def get_ticket(self, ticket_id: int) -> Ticket | None:
        return self._db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def get_by_cod_ticket(self, cod_ticket: str) -> Ticket | None:
        return (
            self._db.query(Ticket)
            .filter(Ticket.cod_ticket == cod_ticket)
            .first()
        )

    def create_ticket(self, data: ticket_schema.TicketCreate) -> Ticket:
        ticket = Ticket(
            cod_ticket=data.cod_ticket,
            descricao=data.descricao,
            responsavel=data.responsavel,
            data_atualizacao=data.data_atualizacao,
        )
        self._db.add(ticket)
        self._db.commit()
        self._db.refresh(ticket)
        return ticket

    def update_ticket(self, ticket_id: int, data: ticket_schema.TicketCreate) -> Ticket | None:
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return None

        ticket.cod_ticket = data.cod_ticket
        ticket.descricao = data.descricao
        ticket.responsavel = data.responsavel
        ticket.data_atualizacao = data.data_atualizacao

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

    # ========= Importação Excel =========

    def upsert_from_import(self, row: ticket_schema.TicketImportRow) -> tuple[Ticket, str]:
        """
        Importa/atualiza um ticket a partir de uma linha do Excel.

        - Se cod_ticket não existe -> cria
        - Se cod_ticket existe:
            - se data_atualizacao do Excel for mais recente -> atualiza
            - caso contrário -> não mexe

        Retorna (ticket, ação) onde ação ∈ {"created", "updated", "skipped"}.
        """
        ticket = self.get_by_cod_ticket(row.cod_ticket)

        excel_dt = row.data_atualizacao
        if isinstance(excel_dt, datetime) and excel_dt.tzinfo is None:
            excel_dt = excel_dt.replace(tzinfo=LOCAL_TZ)

        if ticket is None:
            ticket = Ticket(
                cod_ticket=row.cod_ticket,
                descricao=row.descricao,
                responsavel=row.responsavel,
                data_atualizacao=excel_dt,
            )
            self._db.add(ticket)
            self._db.commit()
            self._db.refresh(ticket)
            return ticket, "created"

        # Caso exista, atualize
        db_dt = ticket.data_atualizacao

        if excel_dt is None:
            return ticket, "skipped"

        if isinstance(db_dt, datetime) and db_dt.tzinfo is None:
            db_dt = db_dt.replace(tzinfo=LOCAL_TZ)

        if db_dt is not None and db_dt >= excel_dt:
            return ticket, "skipped"

        ticket.descricao = row.descricao
        ticket.responsavel = row.responsavel
        ticket.data_atualizacao = excel_dt

        self._db.commit()
        self._db.refresh(ticket)
        return ticket, "updated"