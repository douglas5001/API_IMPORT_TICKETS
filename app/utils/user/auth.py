# app/utils/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi.security import OAuth2PasswordBearer
from pytest import Session
from app.config.database import get_db
from app.models.user.user_model import User
from app.utils.user.jwt_utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
SECRET_KEY = "super-secret-key"   # coloque no .env depois
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()


# ==========================
#  Gera Token JWT
# ==========================
def create_access_token(
    *,
    username: str,
    roles: List[str],
    permissions: List[str],
    expires_delta: Optional[timedelta] = None,
):
    to_encode = {
        "sub": username,
        "roles": roles,
        "permissions": permissions,
        "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ==========================
#  Obtém usuário do token
# ==========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user
