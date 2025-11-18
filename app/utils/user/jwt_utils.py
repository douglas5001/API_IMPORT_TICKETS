from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from app.config.config import config


def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.secret_key, algorithm="HS256")


def decode_token(token: str):
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
