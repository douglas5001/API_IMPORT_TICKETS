# API_IMPORT_TICKETS


Instalação do banco de dados

````
docker run -d --name postgres_db -e POSTGRES_USER=root -e POSTGRES_PASSWORD=SenhaSuperForte1234 -e POSTGRES_DB=postgres_db -p 5432:5432 postgres:15
````

Inicializar api
```
uvicorn app.main:app --reload
```

### Para fazer uso do Alembic

```
alembic revision --autogenerate -m "criação da tabela de tickets"
```

```
alembic upgrade head
```