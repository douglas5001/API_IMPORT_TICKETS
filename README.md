# API_IMPORT_TICKETS



### Instrução de uso (PRODUÇÃO)

- [Como instalar na maquina e testar](./INSTRUCAO.md)

----


### OBS
O projeto está atualmente configurado para realizar o deploy em:
`http://147.93.183.190:8001/docs`

Lá você pode ver os endpoints configurados

**Funcionamento do CI/CD:** Basta realizar um commit na branch main para que o processo de CI/CD seja executado automaticamente.

![alt text](image/image.png)


# Inicialização do projeto em ambiente DEV

Instalação do banco de dados

````
docker run -d --name postgres_db -e POSTGRES_USER=root -e POSTGRES_PASSWORD=SenhaSuperForte1234 -e POSTGRES_DB=postgres_db -p 5432:5432 postgres:15
````

### Configure o `.env`

Coloquei as credenciasi da GoogleCloud propositalmente.
```
DATABASE_URL=postgresql+psycopg2://root:SenhaSuperForte1234@localhost:5432/postgres_db


GOOGLE_CLIENT_ID=1020602488853-u5ivmee510retjgfdnp48tnqkiuorcr2.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=http://localhost:8001/api/v1/auth/google/callback

SECRET_KEY=eqfvgergfejyrnbadvsrryutk435
ACCESS_TOKEN_EXPIRE_MINUTES=60
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
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Instalação do serviço em produção
Caso queira executar o projeto para produção basta inicializar o docker-compose.yml

```
docker compose up -d
```

## Instruções de utilização.
Você pode acassar atraves do Swagger `http://127.0.0.1:8001/docs` ou pelo servidor remoto onde foi feito o deploy `http://147.93.183.190:8001/docs`

### OPÇÃO 2

Pode importar o arquivo `API IMPORTAÇÃO.postman_collection.json` que deixei no diretorio e você terá as rotas prontas e com os dados para executar

![alt text](image/image-1.png)
