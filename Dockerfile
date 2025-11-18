FROM python:3.12-slim

# Evita problemas de buffering e timezone
ENV PYTHONUNBUFFERED=1 \
    TZ=America/Sao_Paulo

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório da aplicação
WORKDIR /app

# Copia requirements primeiro (cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o projeto inteiro
COPY . .

# Porta da API
EXPOSE 8001

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
