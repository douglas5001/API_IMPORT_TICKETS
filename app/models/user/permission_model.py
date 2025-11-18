from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

# Tabela associativa Profile ↔ Permission
profile_permissions = Table(
    "profile_permissions",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profile.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id"), primary_key=True),
)


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(80), unique=True, nullable=False)

    profiles = relationship(
        "Profile",
        secondary=profile_permissions,
        back_populates="permissions",
        lazy="joined",
    )
