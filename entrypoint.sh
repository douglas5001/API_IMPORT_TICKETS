#!/bin/sh

echo "⏳ Aguardando o PostgreSQL ficar disponível..."
sleep 3

echo "🚀 Executando migrações Alembic..."
alembic upgrade head

echo "▶️ Inicializando a API FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
