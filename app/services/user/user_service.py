# app/services/user/user_service.py
from sqlalchemy.orm import Session
from app.repositories.user.user_repository import UserRepository
from app.models.user.user_model import User


class UserService:
    def __init__(self, session: Session):
        self._repo = UserRepository(session)

    def create_or_get_google_user(self, user_info: dict) -> User:
        """
        Cria o usuário caso não exista, ou retorna o existente.
        Sempre usa o perfil GUEST para novos logins Google.
        """
        email = user_info["email"]
        name = user_info.get("name", email)

        user = self._repo.get_by_email(email)
        if user:
            return user

        guest_profile = self._repo.get_guest_profile()

        return self._repo.create_user(
            email=email,
            name=name,
            profile_id=int(guest_profile.id),
        )

