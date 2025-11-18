from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.utils.user.google_auth import get_google_auth_url, login_with_google

router = APIRouter(prefix="/auth")


@router.get("/google")
def google_redirect():
    return {"url": get_google_auth_url()}


@router.get("/google/callback")
def google_callback(request: Request, code: str, db: Session = Depends(get_db)):
    result = login_with_google(code, db)

    return JSONResponse(result)
