[pt-BR]

# Tricorder UI

## Introdução

Esta pasta contem os arquivos relativos ao módulo de frontend da ferramenta Tricorder (Tricorder UI). Este projeto foi gerado utilizando-se [Angular CLI](https://github.com/angular/angular-cli), versão 19.1.5. Este módulo pode ser instanciado em conjunto com o restante da ferramenta, através do Docker compose deste repositório. No entanto, é possível instanciá-lo sem utilizar Docker. Para ambos os casos, siga as instruções abaixo.

## Build e execução com Docker

1. Caso se esteja utilizando Docker para execução do módulo, execute o seguinte comando na pasta raíz deste repositório para fazer o build do container:

`docker-compose build frontend`

2. Após isso, execute o monitoramento seguindo o comando abaixo:

`docker-compose run --remove-orphans frontend`

## Execução sem Docker

Para execução da aplicação sem Docker, é necessário possuir o NPM instalado. Caso não o possua, instale-o através do comando `apt-get install npm`.

1. Instale as dependências através do seguinte comando:

`npm install`

2. Instale então o Angular CLI através do seguinte comando:

`npm install -g @angular/cli`

3. Então, faça o build do módulo:

`ng build` 

4. Por fim, execute a aplicação:

`ng serve --host 0.0.0.0`

---

[en-US]

# Tricorder UI

## Introduction

This directory contains files related to the frontend module for the Tricorder tool (Tricorder UI). This project was generated using [Angular CLI](https://github.com/angular/angular-cli), version 19.1.5. This module can be instantiated together with the rest of the tool, through the Docker compose on this repo. However, it is also possible to run it without using Docker. For both cases, follow the instructions below.

## Building and executing with Docker

1.  If you are using Docker to run the module, execute the following command in the root directory of this repository to build the container:

`docker-compose build frontend`

2. After that, start the monitoring process with the command below:

`docker-compose run --remove-orphans frontend`

## Execução sem Docker

To run the application without Docker, you need to have NPM installed. In case you don't, install it through `apt-get install npm`.

1. Install the dependencies with the following command:

`npm install`

2. Then, install Angular CLI through the following command:

`npm install -g @angular/cli`

3. Build the module:

`ng build` 

4. Finally, execute the application:

`ng serve --host 0.0.0.0`