# app/repositories/user/user_repository.py
from sqlalchemy.orm import Session
from app.models.user.user_model import User
from app.models.user.profile_model import Profile


class UserRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_by_email(self, email: str) -> User | None:
        return (
            self._db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_guest_profile(self) -> Profile:
        """
        Obtém o perfil GUEST.
        Se não existir, cria um novo.
        """
        profile = (
            self._db.query(Profile)
            .filter(Profile.name == "GUEST")
            .first()
        )

        if profile:
            return profile

        profile = Profile(name="GUEST")
        self._db.add(profile)
        self._db.commit()
        self._db.refresh(profile)
        return profile

    def create_user(self, *, email: str, name: str, profile_id: int) -> User:
        user = User(
            email=email,
            name=name,
            profile_id=profile_id,
        )

        self._db.add(user)
        self._db.flush()      # garante ID gerado
        self._db.commit()
        self._db.refresh(user)
        return user
