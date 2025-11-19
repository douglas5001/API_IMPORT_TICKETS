#!/bin/sh

echo "⏳ Aguardando o PostgreSQL iniciar..."
sleep 3

echo "🚀 Aplicando migrations Alembic..."
alembic upgrade head

echo "▶️ Iniciando API FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
