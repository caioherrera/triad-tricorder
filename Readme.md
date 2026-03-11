[pt-BR]

# Tricorder (Ferramenta)

## Introdução

Esta pasta contem os arquivos relativos à ferramenta Tricorder. Esta ferramenta possui 4 módulos, que podem ser executados em conjunto por meio do `Docker compose`, ou individualmente:

- *Monitoring*: módulo de monitoramento, responsável pela execução das aplicações sob teste e monitoramento de seu consumo de recursos.
- *Analysis*: módulo de análise, responsável pela execução da DAMICORE e agrupamento dos perfis coletados no monitoramento.
- *Tricorder-Backend*: API que realiza a interface e comunicação entre o frontend e o banco de dados, além de interagir com os módulos de monitoramento e análise.
- *Tricorder-UI*: projeto frontend que fornece uma UI para uso da ferramenta Tricorder. 

Cada módulo possui uma pasta identificada pelo seu nome, com um arquivo `README.md` e instruções específicas para seu uso individual. Além disso, cada módulo possui um arquivo `Dockerfile` com o passo-a-passo para criação de seu container. 

## Instruções para execução dos experimentos da Tricorder dentro do container Docker

Na raíz deste repositório encontra-se um arquivo `docker-compose.yml` com as informações necessárias para que o Docker compose seja capaz de construir os containers da ferramenta.

Siga os passos abaixo para rodar o experimento:

1) Clone este repositório 

`git clone https://github.com/tricorder-lasdpc/tricorder-docker.git`

2) Rode a imagem da Tricorder. Para construir e executar com base no Dockerfile, add --detach para execução em segundo plano.:

`docker-compose up --build --detach`

---

[en-US]

# Tricorder (Tool)

## Introduction

This folder contains the files related to the Tricorder tool. The tool has 4 modules, which can be run together using `Docker compose`, or individually:

- *Monitoring*: monitoring module, responsible for running the applications under test and monitoring their resource consumption.
- *Analysis*: analysis module, responsible for running DAMICORE and grouping the profiles collected during monitoring.
- *Tricorder-Backend*: API that provides the interface and communication between the frontend and the database, and also interacts with the monitoring and analysis modules.
- *Tricorder-UI*: frontend project that provides a UI for using the Tricorder tool.

Each module has a folder identified by its name, with a `README.md` file and specific instructions for individual use. In addition, each module has a `Dockerfile` with step-by-step instructions for creating its container.

## Instructions for running Tricorder experiments inside the Docker container

At the root of this repository, there is a `docker-compose.yml` file with the necessary information for Docker compose to build the tool's containers.

Follow the steps below to run the experiment:

1) Clone this repository

`git clone https://github.com/tricorder-lasdpc/tricorder-docker.git`

2) Run the Tricorder image. To build and run based on the Dockerfile, add --detach to run in the background:

`docker-compose up --build --detach`
