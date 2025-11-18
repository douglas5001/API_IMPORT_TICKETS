from app.models.user.user_model import User
from app.models.user.profile_model import Profile
from sqlalchemy.orm import Session

class UserService:

    def __init__(self, db: Session):
        self.db = db

    def create_or_get_google_user(self, user_info):

        email = user_info["email"]
        name = user_info.get("name", email)

        user = self.db.query(User).filter(User.email == email).first()
        if user:
            return user

        # buscar perfil GUEST
        guest_profile = self.db.query(Profile).filter(Profile.name == "GUEST").first()

        if not guest_profile:
            guest_profile = Profile(name="GUEST")
            self.db.add(guest_profile)
            self.db.commit()

        user = User(
            email=email,
            name=name,
            profile_id=guest_profile.id
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
