from datetime import datetime

from sqlalchemy import String, DateTime, func, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class TicketLog(Base):
    __tablename__ = "ticket_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    ticket_id: Mapped[int | None] = mapped_column(
        ForeignKey("tickets.id"),
        nullable=True,
        index=True,
    )

    cod_ticket: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index=True,
    )

    action: Mapped[str] = mapped_column(String(50), nullable=False)

    before_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    after_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
