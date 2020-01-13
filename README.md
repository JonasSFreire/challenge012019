# Descrição

Serviço em Flask com arquitetura REST para manipular dados de usuários, utilizando containers Docker Postgres e NGINX.


# Sumário de arquivos

```/manage.py```: módulo responsável pela gerência de depenências, migrations e incialização do app;

```/boot.sh```: script para rodar com o Docker, efetua upgrade no Postgres e aguarda o app inciar até o Postgres inciar primeiro;

```/.env```: armazena as variáveis de ambiente do projeto;

```/nginx/default.conf```: configurações do Nginx para execução via Docker;

```/migrations```: arquivos de configuração das migrations para o Postgres.

```/app/__init__.py```: módulo principal, para inicialização do servidor Flask + Blueprints e SQLAlchemy;

```/app/api/resources/users.py```: módulo que contêm todos métodos de acesso e demais regras de negócio para manipulação de dados dos usuários;

```/app/api/models/users.py```: contém os models para execução das migrations dos usuários;

```/app/tests/```: diretório para armazenamento dos testes;

```/app/auth.py```: contêm diretivas de autenticação;

```/app/config.py```: configurações gerais do projeto;

```/app/errors.py```: funções para tratamento de mensagens de erros;

```/app/handlers.py```: funções para manipulação/descrição dos erros;

```/app/tokens.py```: módulo para manipular acessos via token;


# Executando a aplicação

* Instale o Docker: https://docs.docker.com/install/linux/docker-ce/ubuntu/

* Instale o Docker Compose: https://docs.docker.com/compose/install/

* ```$ git clone https://github.com/daltroedu/challenge012019.git```: clone este repositório;

* ```$ cd challenge012019/```: entre nele;

* ```$ docker-compose build```: para compilar os containers (apenas uma vez);

* ```$ docker-compose up```: para executar o aplicação (CTRL+C para sair);

## Sobre a aplicação

Rotas:

```/v1/users/```: rota HTTP com os métodos GET, POST, PUT e DELETE para manipular dados do usuário;

```/v1/token/```: rota HTTP com os métodos POST e DELETE para obter e revogar autenticação do usuário via token;

Portas:
* Flask: 80 (NGINX) produção e 5000 desenvolvimento
* Postgres: 5432

A criação do usuário (POST) não tem autenticação justamente para ser possível criar um e obter a respectiva autenticação. Os métodos GET são acessados por qualquer usuário autenticado via token. PUT e DELETE são permitidos apenas do usuário para ele mesmo.

Utilize o httpie ou outro client para interagir com a aplicação: ```$ sudo apt install httpie```

* Criando novo usuário (POST):
```$ http POST http://localhost/v1/users/ id=1 email=test@test.com password_hash=test name=test```

* Obtendo token para o usuário com e-mail e senha (POST):
```$ http --auth test@test.com:test POST http://localhost/v1/token/```

* Consultando todos os usuários registrados (GET):
```http GET http://localhost/v1/users/ Authorization:"Bearer <token>"```

* Consultando usuário específico (GET)
```http GET http://localhost/v1/users/<id> Authorization:"Bearer <token>"```

* Alterando dados do usuário (PUT):
```http PUT http://localhost/v1/users/<id> name=NovoName Authorization:"Bearer <token>"```

* Revogando token (DELETE):
```http DELETE http://localhost/v1/token/ Authorization:"Bearer <token>"```

* Deletando usuário (DELETE):
```http DELETE http://localhost/v1/users/<id> Authorization:"Bearer <token>"```


## Ambientes Dev e Testing

* ```$ sudo apt update && sudo apt install postgresql postgresql-contrib libpq-dev python3-dev python-psycopg2```: instala o Postgres e respectivas dependências do psycopg2;

* ```$ sudo -i -u postgres```: para entrar com o usuário do Postgres;

* ```# psql```: para acessar o banco de dados;

* ```# ALTER USER postgres WITH PASSWORD 'postgres';```: define a senha do usuário padrão;

* ```# CREATE DATABASE project;```: cria database de dev;

* ```# CREATE DATABASE testing;```: cria database de testes;

* ```# GRANT ALL PRIVILEGES ON DATABASE project TO postgres;```: conceda privilégios ao usuário padrão para o novo database de dev;

* ```# GRANT ALL PRIVILEGES ON DATABASE testing TO postgres;```: conceda privilégios ao usuário padrão para o novo database de testes;

* ```$ sudo apt install -y python-pip3```: instala o pip3;

* ```$pip3 install virtualenv```: instala a virtualenv;

* ```$ python3 -m virtualenv venv```: cria um ambiente virual;

* ```$ source venv/bin/activate```: entra no ambiente virtual;

* ```$ pip3 install -r requirements.txt```: instala as depenências do projeto;

* Executando os testes: ```$ pytest app/tests/users.py```

* Executando a aplicação: ```$ flask run``` (altere ```FLASK_CONFIG``` para "development" em ```.env```);

* ```$ deactivate```: sai do ambiente de virtual;


## Migrations

* ```$ flask db init```: inicia o projeto;

* ```$ flask db migrate```: atualiza os models;

* ```$ flask db upgrade```: migra os dados para o Postgres.
