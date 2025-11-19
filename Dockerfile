FROM python:3.12-slim

# Evita problemas de buffering e timezone
ENV PYTHONUNBUFFERED=1 \
    TZ=America/Sao_Paulo

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Diretório do app
WORKDIR /app

# Copia apenas requerimentos primeiro
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do projeto
COPY . .

RUN chmod +x /app/entrypoint.sh

# Expõe a porta interna onde o Uvicorn irá rodar
EXPOSE 8000

# Inicia o servidor FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]

