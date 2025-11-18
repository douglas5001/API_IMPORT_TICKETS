from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.utils.user.google_auth import get_google_auth_url, login_with_google
from app.services.user.user_service import UserService

router = APIRouter(prefix="/auth")


@router.get("/google")
def google_redirect():
    return {"url": get_google_auth_url()}


@router.get("/google/callback")
def google_callback(request: Request, code: str, db: Session = Depends(get_db)):
    result = login_with_google(code, db)

    # Aqui você pode redirecionar de volta para o frontend
    # ou simplesmente retornar o token
    return JSONResponse(result)


@router.get("/index", response_class=HTMLResponse)
def index_page(request: Request, user_id: int = 0, email: str = "", name: str = ""):

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <meta charset="UTF-8">
    </head>

    <body style="font-family: Arial; padding: 20px;">

        <h2>Usuário Logado</h2>
        <pre>
ID: {user_id}
Email: {email}
Nome: {name}
        </pre>

        <hr>

        <h2>Deletar Ticket</h2>
        <label>ID do ticket:</label>
        <input id="ticketId" type="number">

        <button onclick="deletar()">Deletar</button>

        <br><br>
        <pre id="resultado"></pre>

        <script>
            async function deletar() {{
                const id = document.getElementById("ticketId").value;

                const response = await fetch(`/api/v1/tickets/${{id}}`, {{
                    method: "DELETE"
                }});

                const data = await response.json();
                document.getElementById("resultado").innerText = JSON.stringify(data, null, 4);
            }}
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html)
