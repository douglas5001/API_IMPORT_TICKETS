from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.user.permission_model import profile_permissions

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(80), unique=True, nullable=False)

    permissions = relationship(
        "Permission",
        secondary=profile_permissions,
        back_populates="profiles",
        lazy="joined",
    )
