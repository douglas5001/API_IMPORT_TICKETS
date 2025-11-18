from datetime import datetime
from zoneinfo import ZoneInfo

def test_create_ticket(client):
    payload = {
        "cod_ticket": "RITM0001",
        "descricao": "Teste de criação",
        "responsavel": "Douglas",
        "data_atualizacao": "2025-01-18T22:00:00"
    }

    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["cod_ticket"] == "RITM0001"
    assert data["descricao"] == "Teste de criação"


def test_get_ticket(client):
    resp = client.post("/api/v1/tickets", json={
        "cod_ticket": "RITM0002",
        "descricao": "Consultar",
        "responsavel": "Douglas",
        "data_atualizacao": "2025-01-18T22:00:00"
    })

    assert resp.status_code == 200
    ticket_id = resp.json()["id"]

    # consulta
    response = client.get(f"/api/v1/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["cod_ticket"] == "RITM0002"


def test_unique_cod_ticket(client):
    payload = {
        "cod_ticket": "RITM_DUP",
        "descricao": "Primeira",
        "responsavel": "Douglas",
        "data_atualizacao": "2025-01-18T22:00:00"
    }

    r1 = client.post("/api/v1/tickets", json=payload)
    assert r1.status_code == 200

    # duplicado → deve retornar erro 400
    r2 = client.post("/api/v1/tickets", json=payload)
    assert r2.status_code == 400
    assert "já existe" in r2.json()["detail"].lower()
