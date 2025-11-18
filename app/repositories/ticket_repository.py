from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ticket_model import Ticket
from app.models.ticket_log_model import TicketLog
from app.schemas import ticket_schema

LOCAL_TZ = ZoneInfo("America/Sao_Paulo")


class TicketRepository:
    def __init__(self, session: Session):
        self._db = session

    # ================= Helpers de serialização / log =================

    def _ticket_to_dict(self, ticket: Ticket | None) -> dict | None:
        """
        Converte um Ticket em dict com valores JSON-serializáveis.
        (Datetime vira string ISO, etc.)
        """
        if ticket is None:
            return None

        def _dt(v: datetime | None):
            if v is None:
                return None
            # garante string ISO (ISO 8601)
            return v.isoformat()

        return {
            "id": ticket.id,
            "cod_ticket": ticket.cod_ticket,
            "descricao": ticket.descricao,
            "responsavel": ticket.responsavel,
            "data_atualizacao": _dt(ticket.data_atualizacao),
            "created_at": _dt(ticket.created_at),
            "updated_at": _dt(ticket.updated_at),
        }

    def _log_action(
        self,
        *,
        action: str,
        ticket: Ticket | None = None,
        before: dict | None = None,
        after: dict | None = None,
    ) -> None:
        """
        Registra uma linha na tabela ticket_logs.
        """
        log = TicketLog(
            ticket_id=ticket.id if ticket else None,
            cod_ticket=ticket.cod_ticket if ticket else None,
            action=action,
            before_data=before,
            after_data=after,
        )
        self._db.add(log)

    # ================= CRUD básico =================

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
        existing = self.get_by_cod_ticket(data.cod_ticket)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"cod_ticket '{data.cod_ticket}' já existe",
            )

        ticket = Ticket(
            cod_ticket=data.cod_ticket,
            descricao=data.descricao,
            responsavel=data.responsavel,
            data_atualizacao=data.data_atualizacao,
        )

        self._db.add(ticket)
        # Gera o ID antes do log, mas ainda sem commit
        self._db.flush()

        after = self._ticket_to_dict(ticket)
        self._log_action(action="CREATE", ticket=ticket, before=None, after=after)

        self._db.commit()
        self._db.refresh(ticket)
        return ticket

    def update_ticket(
        self,
        ticket_id: int,
        data: ticket_schema.TicketCreate,
    ) -> Ticket | None:
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return None

        before = self._ticket_to_dict(ticket)

        ticket.cod_ticket = data.cod_ticket
        ticket.descricao = data.descricao
        ticket.responsavel = data.responsavel
        ticket.data_atualizacao = data.data_atualizacao

        self._db.flush()

        after = self._ticket_to_dict(ticket)
        self._log_action(action="UPDATE", ticket=ticket, before=before, after=after)

        self._db.commit()
        self._db.refresh(ticket)
        return ticket

    def delete_ticket(self, ticket_id: int) -> bool:
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False

        before = self._ticket_to_dict(ticket)

        self._db.delete(ticket)
        # log ainda pode usar os dados em memória
        self._log_action(action="DELETE", ticket=ticket, before=before, after=None)

        self._db.commit()
        return True

    # ========= Importação Excel =========

    def upsert_from_import(
        self,
        row: ticket_schema.TicketImportRow,
    ) -> tuple[Ticket, str]:
        """
        Importa/atualiza um ticket a partir de uma linha do Excel.

        - Se cod_ticket não existe -> cria (created)
        - Se cod_ticket existe:
            - se data_atualizacao do Excel for mais recente -> atualiza (updated)
            - caso contrário -> não mexe (skipped)

        Retorna (ticket, ação) onde ação ∈ {"created", "updated", "skipped"}.
        """
        ticket = self.get_by_cod_ticket(row.cod_ticket)

        excel_dt = row.data_atualizacao
        if isinstance(excel_dt, datetime) and excel_dt.tzinfo is None:
            excel_dt = excel_dt.replace(tzinfo=LOCAL_TZ)

        # ---- NOVO: CREATE via import ----
        if ticket is None:
            ticket = Ticket(
                cod_ticket=row.cod_ticket,
                descricao=row.descricao,
                responsavel=row.responsavel,
                data_atualizacao=excel_dt,
            )
            self._db.add(ticket)
            self._db.flush()

            after = self._ticket_to_dict(ticket)
            self._log_action(
                action="IMPORT_CREATED",
                ticket=ticket,
                before=None,
                after=after,
            )

            self._db.commit()
            self._db.refresh(ticket)
            return ticket, "created"

        # ---- Já existia: decidir se atualiza ou pula ----
        db_dt = ticket.data_atualizacao

        if excel_dt is None:
            # Loga que foi ignorado
            before = self._ticket_to_dict(ticket)
            self._log_action(
                action="IMPORT_SKIPPED",
                ticket=ticket,
                before=before,
                after=before,
            )
            self._db.commit()
            return ticket, "skipped"

        if isinstance(db_dt, datetime) and db_dt.tzinfo is None:
            db_dt = db_dt.replace(tzinfo=LOCAL_TZ)

        if db_dt is not None and db_dt >= excel_dt:
            # mantemos o registro, mas podemos registrar o skip também
            before = self._ticket_to_dict(ticket)
            self._log_action(
                action="IMPORT_SKIPPED",
                ticket=ticket,
                before=before,
                after=before,
            )
            self._db.commit()
            return ticket, "skipped"

        # Atualiza com dados mais novos
        before = self._ticket_to_dict(ticket)

        ticket.descricao = row.descricao
        ticket.responsavel = row.responsavel
        ticket.data_atualizacao = excel_dt

        self._db.flush()

        after = self._ticket_to_dict(ticket)
        self._log_action(
            action="IMPORT_UPDATED",
            ticket=ticket,
            before=before,
            after=after,
        )

        self._db.commit()
        self._db.refresh(ticket)
        return ticket, "updated"
