# Instalação e testes
Por meio desse documento vou realizar o passo a passo da instalação do projeto até aos testes


### Requisitos

- Docker instalado
- Docker-compose instaldo
- Python 3.12.10


Acesse o Powershell e execute
````
git clone https://github.com/douglas5001/API_IMPORT_TICKETS.git
````


crie o arquivo `.env` e coloque as informações abaixo
````
DATABASE_URL=postgresql+psycopg2://root:SenhaSuperForte1234@localhost:5432/postgres_db


GOOGLE_CLIENT_ID=1020602488853-u5ivmee510retjgfdnp48tnqkiuorcr2.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=http://localhost:8001/api/v1/auth/google/callback

SECRET_KEY=eqfvgergfejyrnbadvsrryutk435
ACCESS_TOKEN_EXPIRE_MINUTES=60
````

execute o comando docker estando dentro do diretorio do projeto
````
docker-compose up -d
````

verifique se rodou e que os containers estao com porta exposta
```
docker ps
```

Vai retornar algo como

![alt text](image/imagee.png)

Estrutura esperada no banco de dados
![alt text](image/image-3.png)

---

Vamos realizar os teste utilizadno a ferramenta `Postman`, mas o mesmo funciona com o Swagger em `http://localhost:8001/docs`

<br>

## Testes

### Ordem de testes

- Vamos criar uma unica tarefa utilizando a rota `POST` `http://127.0.0.1:8001/api/v1/tickets`
- Vamos realizar a importação de tarefas em massa via Excel utizando a rota `POST` `http://127.0.0.1:8001/api/v1/tickets/import`
- Vamos listar uma unica tarefa utilizando a rota `GET` `http://127.0.0.1:8001/api/v1/tickets/ID`
- Vamos listar todas tarefas utilizando a rota `GET` `http://127.0.0.1:8001/api/v1/tickets` (Ela não tem paginação)
- Vamos realizar uma alteração em um indice utilizando a rota `PUT` `http://127.0.0.1:8001/api/v1/tickets/ID`
- Vamos gerar um token para logar com a conta da google utilizadno a rota `GET` `http://localhost:8001/api/v1/auth/google``
- Apartir do token gerado após authenticação vamos colocar ele como valor do paremetro `Authorization` e o valor `Bearer + TOKEN` e vamos utilizar a rota protegida `DELETE` `http://127.0.0.1:8001/api/v1/tickets/ID`

---

### CRIAR UMA TAREFA

**METODO:** POST

**ENDPOINT:** http://127.0.0.1:8001/api/v1/tickets

Carregue no BODY o JSON
```` json
{
  "cod_ticket":"ABC",
  "descricao": "Teste de descrição",
  "responsavel": "Douglas Portella"
}
````
Exemplo:
![alt text](image/image-4.png)

---

### IMPORTAÇÃO DE TAREFAS EM MASSA
  
**METODO:** POST

**ENDPOINT:** http://127.0.0.1:8001/api/v1/tickets/import

Vá em Body e selecione o método `form-data`, utilize a variavel `file` e o tipo `file` e deixe anexado o documento que esta no repositorio `tickets.xlsx`

Exemplo:
![alt text](image/image-5.png)

**OBS:** Para a importação do excel será capturado apenas as colunas `cod_ticket`, `responsavel` e `data_atualizacao` e tanto inserção, delete, update, ou quando é tentativa de insersão, isso tudo é salvo em uma tabela de logs, conforme requisitado.


---

### LISTAR TAREFA UNICA
  
**METODO:** GET

**ENDPOINT:** http://127.0.0.1:8001/api/v1/tickets/6

![alt text](image/image-6.png)


---

### LISTAR TODAS TAREFAS
  
**METODO:** GET

**ENDPOINT:** http://127.0.0.1:8001/api/v1/tickets

![alt text](image/image-7.png)


---

### ALTERAÇÃO DE TAREFA
  
**METODO:** PUT

**ENDPOINT:** http://127.0.0.1:8001/api/v1/tickets/6

Json no Body
``` json
{
    "cod_ticket": "RITM0951323",
    "descricao": "Instalação dos módulos de segurança dos bancos. \n\nItaú, BB, Bradesco",
    "responsavel": "Lindberg Pereira Severo"
}
```
EXEMPLO: 

![alt text](image/image-8.png)

---

### LOGIN COM A GOOGLE
  
**METODO:** GET

**ENDPOINT:** http://localhost:8001/api/v1/auth/google

**OBS:** QUando ralizar o `GET` vai retornar uma URL, você copia essa url e cola no navegador, após isso você realiza a Authenticação com uma conta da google, depois sera direcionado para uma pagina com um token, vamos usar esse token para liberar a rota protegida `DELETE`:`http://127.0.0.1:8001/api/v1/tickets/6`

Exemplo:
![alt text](image/image-9.png)

Copiamos o link e acessaremos pelo navegador, vou logar com a conta rocketStack
![alt text](image/image-10.png)

Após iso um token me é gerado, vamos usar ele para acessar uma rota protegida
![alt text](image/image-11.png)

Caso o usuario não exista, ele é criado no banco, também recebera o perfil GUEST e a permissao GUEST, a nossa rota protegida só pode ser acessada se o perfil tiver a permission GUEST, este é o conceito de RBAC
![alt text](image/image-12.png)

---

### DELETAR TICKET (ROTA PROTEGIDA)
  
**METODO:** DELETE

**ENDPOINT:** http://127.0.0.1:8001/api/v1/tickets/6

**HEADERS:**
- key: Authorization
- Value: Bearer + Token
![alt text](image/image-13.png)

Ao realizar o `DELETE` vai nos retornar
![alt text](image/image-15.png)

Caso Token invalido retorna
![alt text](image/image-16.png)

Caso não tenha a permissão retorna
![alt text](image/image-14.png)


---

### LOGS
  
**LOGS:** Qualquer operação realizada que afete o estado da tabela tikets é registrado na tabela `ticket_logs``

- Com isso conseguimos saber tudo que foi alterado e inclusive saber o status anterior.

- Também podemos implementar quem alterou os estados capturando o valor das rules do token do usuário

Como pode ver tem logs de todos os tipos `CREATE`, `UPDATE`, `DELETE`, `IMPORT_CREATED` e `IMPORT_SKIPPED`

![alt text](image/bancologs.png)

---
### Status Api

Ultimo requisito é o endpoint de status, inclusive é utilizado ao final do deploy para validar se o serviço esta operante.

![alt text](image/image59.png)

