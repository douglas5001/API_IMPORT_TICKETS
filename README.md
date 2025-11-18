# API_IMPORT_TICKETS

O projeto está atualmente configurado para realizar o deploy em:
`http://147.93.183.190:8001/docs`

Basta realizar um commit na branch main para que o processo de CI/CD seja executado automaticamente.

![alt text](image.png)


# Inicialização do projeto em ambiente DEV

Instalação do banco de dados

````
docker run -d --name postgres_db -e POSTGRES_USER=root -e POSTGRES_PASSWORD=SenhaSuperForte1234 -e POSTGRES_DB=postgres_db -p 5432:5432 postgres:15
````

### Configure o `.env`
```
DATABASE_URL=postgresql+psycopg2://root:SenhaSuperForte1234@localhost:5432/postgres_db
```

### Inicialize o Venv
````
python -m venv .venv
````

### Instale as dependências
````
install -r requirements.txt
````

### Crie as tabelas via Alembic
```
alembic revision --autogenerate -m "criação da tabela de tickets"
```

### Rode a migração
```
alembic upgrade head
```

### Inicializar api
```
uvicorn app.main:app --reload
```

## Instalação do serviço em produção
Caso queira executar o projeto para produção basta inicializar o docker-compose.yml

```
docker compose up -d
```

## Instruções de utilização.
Você pode acassar atraves do Swagger `http://127.0.0.1:8000/docs` ou pelo servidor remoto onde foi feito o deploy `http://147.93.183.190:8001/docs`

### OPÇÃO 2

Pode importar o arquivo `API IMPORTAÇÃO.postman_collection.json` que deixei no diretorio e você terá as rotas prontas e com os dados para executar

![alt text](image-1.png)
