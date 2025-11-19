import requests
from fastapi import HTTPException
from app.config.config import config
from sqlalchemy.orm import Session
from app.models.user.user_model import User
from app.models.user.profile_model import Profile
from app.models.user.permission_model import Permission
from app.utils.user.jwt_utils import create_access_token

## Nao vou por no .env porque é só protótipo
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"  # nosec B105
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"  # nosec B105


def get_google_auth_url() -> str:
    return (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={config.google_client_id}"
        f"&redirect_uri={config.google_redirect_uri}"
        "&access_type=offline"
        "&prompt=consent"
        "&scope=openid%20email%20profile%20https://www.googleapis.com/auth/userinfo.email%20https://www.googleapis.com/auth/userinfo.profile"
    )


def exchange_code_for_token(code: str) -> dict:
    data = {
        "code": code,
        "client_id": config.google_client_id,
        "client_secret": config.google_client_secret,
        "redirect_uri": config.google_redirect_uri,
        "grant_type": "authorization_code",
    }

    r = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=10)

    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao trocar code pelo token")

    return r.json()


def get_google_user_info(access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(GOOGLE_USERINFO_URL, headers=headers, timeout=10)

    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao buscar informações do Google")

    return r.json()


def login_with_google(code: str, db: Session):

    token_data = exchange_code_for_token(code)
    user_info = get_google_user_info(token_data["access_token"])

    print("DEBUG USERINFO:", user_info)

    email = user_info.get("email")
    name = user_info.get("name", "Google User")

    if not email:
        raise HTTPException(status_code=400, detail="Google não retornou o email. Verifique escopos.")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        # garante perfil guest
        profile = db.query(Profile).filter(Profile.name == "GUEST").first()

        if not profile:
            perm = Permission(name="GUEST")
            db.add(perm)
            db.flush()

            profile = Profile(name="GUEST", permissions=[perm])
            db.add(profile)
            db.flush()

        user = User(
            name=name,
            email=email,
            password="",  # nosec B106
            is_admin=False,
            profile_id=profile.id
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "profile": user.profile.name
        }
    }
