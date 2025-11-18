from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256
from app.config.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=True)
    profile = relationship("Profile")

    def encrypt_password(self):
        self.password = pbkdf2_sha256.hash(self.password)

    def verify_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)
    
    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "profile_id": self.profile_id,
        }
