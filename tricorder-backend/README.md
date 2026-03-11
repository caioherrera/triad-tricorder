[pt-BR]

# Tricorder Backend

## Introdução

Esta pasta contem os arquivos relativos ao módulo de backend da ferramenta Tricorder. Este módulo é responsável por interagir com o banco de dados da ferramenta, expondo APIs para leitura, escrita e atualização de dados, além de controlar a execução dos módulos de monitoramento e análise. 

O módulo de backend pode ser utilizado em conjunto com a ferramenta, onde funciona como uma API desenvolvida em Flask para receber requisições HTTP através dos vários endpoints expostos. Neste tipo de execução, o módulo recebe requisições do módulo de frontend, e também interage enviando/recebendo requisições dos módulos de monitoramento e análise.

Além disso, o módulo de backend também pode ser executado de forma *stand-alone*, sem depender dos outros módulos da ferramenta. Para este tipo de execução, siga as instruções abaixo.

## Build e execução com Docker

1. Caso se esteja utilizando Docker para execução do módulo, execute o seguinte comando na pasta raíz deste repositório para fazer o build do container:

`docker-compose build backend`

2. Após isso, execute o container seguindo o comando abaixo:

`docker-compose run -p 5000:5000 --remove-orphans backend python3 -m flask run`

3. A partir daí, é possível acessar o módulo de backend a partir do link `http://127.0.0.1:5000/<endpoint_desejado>`

## Execução sem Docker

Para execução da aplicação sem Docker, é necessário possuir Python3 e pip3 instalado. Atenção: talvez você precise fazer os próximos passos com usuário root.

1. Instale as dependências através do seguinte comando (na pasta raíz do repositório):

`pip install -r ./tricorder-backend/requirements.txt`

2. Além disso, defina variáveis de ambiente `TRICORDER_DATABASE_PATH` e `TRICORDER_DATABASE_INIT_SCRIPT` indicando, respectivamente, o local do arquivo SQLite (banco de dados), e o local onde está o script que o inicializa:

`export TRICORDER_DATABASE_PATH=/tmp/example/tricorder.db`
`export TRICORDER_DATABASE_INIT_SCRIPT=/tmp/example/init_script.sql`

3. Então, execute a aplicação:

`python3 -m flask run`

---

[en-US]

# Tricorder Backend

## Introduction

This folder contains the files related to the backend module of the Tricorder tool. This module is responsible for interacting with the tool's database, exposing APIs for reading, writing, and updating data, as well as controlling the execution of the monitoring and analysis modules.

The backend module can be used together with the tool, functioning as an API developed in Flask to receive HTTP requests through the various exposed endpoints. In this setup, the module receives requests from the frontend module and also interacts by sending/receiving requests from the monitoring and analysis modules.

Additionally, the backend module can also be run *stand-alone*, without depending on the other modules of the tool. For this type of execution, follow the instructions below.

## Building and running with Docker

1. If you are using Docker to run the module, execute the following command in the root folder of this repository to build the container:

`docker-compose build backend`

2. After that, start the container with the command below:

`docker-compose run -p 5000:5000 --remove-orphans backend python3 -m flask run`

3. From there, you can access the backend module at `http://127.0.0.1:5000/<desired_endpoint>`

## Running without Docker

To run the application without Docker, you need to have Python3 and pip3 installed. Note: you may need to perform the following steps as root.

1. Install the dependencies with the following command (in the repository root folder):

`pip install -r ./tricorder-backend/requirements.txt`

2. Also, set the environment variables `TRICORDER_DATABASE_PATH` and `TRICORDER_DATABASE_INIT_SCRIPT`, indicating respectively the location of the SQLite file (database) and the location of the script that initializes it:

`export TRICORDER_DATABASE_PATH=/tmp/example/tricorder.db`
`export TRICORDER_DATABASE_INIT_SCRIPT=/tmp/example/init_script.sql`

3. Then, run the application:

`python3 -m flask run`