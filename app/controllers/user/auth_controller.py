from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.utils.user.google_auth import get_google_auth_url, login_with_google

router = APIRouter(prefix="/auth")


@router.get("/google")
def google_redirect():
    """
    Realiza login utilizando os serviços da Google Cloud, ao realizar um GET ele vai te retornar uma URL, você copia ela e cola no navegador, depois loga com uma conta da google e vai te gerar um token, você vai usar este token para acessar o metodo DELETE
    
    OBS: Esse endPoint não vai funcionar se tiver em um servidor, pois lá na Google Cloud precisarei configurar um dominio de confiança
    """
    return {"url": get_google_auth_url()} 


@router.get("/google/callback")
def google_callback(request: Request, code: str, db: Session = Depends(get_db)):
    """
    Retorna um json do login realizado através da Google
    """
    result = login_with_google(code, db)

    return JSONResponse(result)

