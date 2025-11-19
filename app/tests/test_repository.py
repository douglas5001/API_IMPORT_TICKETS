from app.repositories.ticket.ticket_repository import TicketRepository
from app.models.ticket.ticket_model import Ticket
from app.config.database import SessionLocal


def test_upsert_import_create():
    db = SessionLocal()

    repo = TicketRepository(session=db)

    ticket = repo.create_ticket(
        data=Ticket(
            cod_ticket="AAA123",
            descricao="Teste",
            responsavel="Lucas",
            data_atualizacao=None
        )
    )

    assert ticket.id is not None
    assert ticket.cod_ticket == "AAA123"

    db.close()
