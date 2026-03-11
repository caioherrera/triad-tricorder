[pt-BR]

# Análise

## Introdução

Esta pasta contem os arquivos relativos ao módulo de análise da ferramenta Tricorder. Este módulo é responsável por, dado um conjunto de arquivos CSV representando perfis de consumo de recursos de uma aplicação monitorada, executar a DAMICORE e agrupar os perfis, na busca por anomalias. Esta execução pode ou não depender de uma pasta com perfis de referências.

O módulo de análise pode ser utilizado em conjunto com a ferramenta, onde funciona como uma API desenvolvida em Flask para receber requisições de análise através do endpoint `[POST]] /api/analysis`. Neste tipo de execução, o módulo envia uma requisição para `[POST] <backend>/api/analysis/status` com um status de sua análise após cada execução,e para `[POST] <backend>/api/analysis/result` ao final de uma etapa de análise, com o resultado completo desta.

Além disso, o módulo de análise também pode ser executado de forma *stand-alone*, sem depender dos outros módulos da ferramenta. Para este tipo de execução, siga as instruções abaixo.

## Parâmetros do módulo

Para uma execução *stand-alone*, os seguintes parâmetros são previstos:

- `--profiles-folder`: Caminho para o diretório com arquivos de perfis de consumo a serem agrupados. Obrigatório.
- `--ref-folder`: Caminho para o diretório com arquivos de perfis de consumo tidos como referência. Opcional.
- `--log-detail-level`: Valor inteiro no intervalo [0, 2] representando o nível de detalhamento dos logs, sendo 0 = nenhum log, 1 = poucos logs, 2 = todos os logs. Opcional, com valor padrão em 2.

## Build e execução com Docker

1. Caso se esteja utilizando Docker para execução do módulo, execute o seguinte comando na pasta raíz deste repositório para fazer o build do container:

`docker-compose build analysis`

2. Após isso, execute a análise seguindo o comando abaixo:

`docker-compose run --remove-orphans analysis python3 app.py [-h] --profiles-folder PROFILES_FOLDER [--ref-folder REF_FOLDER] [--log-detail-level {0,1,2}]`

## Execução sem Docker

Para execução da aplicação sem Docker, é necessário possuir Python3 e pip3 instalado. Atenção: talvez você precise fazer os próximos passos com usuário root.

1. Execute o arquivo `bootstrap.sh` para instalação de algumas dependências do módulo de análise:

`./analysis/bootstrap.sh`

2. Instale as dependências do módulo através do seguinte comando (na pasta raíz do repositório):

`pip install -r ./analysis/requirements.txt`

3. Instale as dependências da DAMICORE através do seguinte comando (na pasta raíz do repositório):

`pip install -r ./analysis/damicore_requirements.txt`

4. Então, execute a aplicação:

`python3 app.py [-h] --profiles-folder PROFILES_FOLDER [--ref-folder REF_FOLDER] [--log-detail-level {0,1,2}]`

5. Caso queira utilizar o módulo por meio da API Flask, execute-o a partir do comando:

`python3 -m flask run`

## Exemplo de linha de comando

Abaixo um exemplo de execução do módulo de análise com duas pastas arbitrárias:

`python3 app.py --profiles-folder ../profiles/e55c9410-b953-45b8-bbe3-324ca6294fe7 --ref-folder ../profiles/a6b32106-2b72-424b-8516-19736c76b277`

---

[en-US]

# Analysis

## Introduction

This directory contains files related to the analysis module for the Tricorder tool. This module is responsible for, given a set of CSV files representing resource consumption profiles for a monitored application, executes DAMICORE and groups the profiles in search for anomalies. This execution may or may not rely on a folder with reference profiles.

The analysis module can be used through the Tricorder tool, where it will work as a Flask API to receive analysis requests through the endpoint `[POST]] /api/analysis`. In this execution setup, the module will send a request to `[POST] <backend>/api/analysis/status` with an analysis status after each execution, and to `[POST] <backend>/api/analysis/result` at the end of the analysis step, with the final result for the task.

Aside from that, the analysis module can also be executed stand-alone, without relying on the tool and its modules. For this type of execution, follow the instructions below.

## Module parameters

For stand-alone execution, the following parameters are available:

- `--profiles-folder`: Path to a folder with the resource consumption profiles files to be grouped. Required.
- `--ref-folder`: Path to a folder with the resource consumption profiles taken as reference. Optional.
- `--log-detail-level`: Integer value in the range [0, 2] representing the log detail level, where 0 = no logs, 1 = minimal logs, 2 = all logs. Optional, default is 2.

## Building and executing with Docker

1. If you are using Docker to run the module, execute the following command in the root directory of this repository to build the container:

`docker-compose build analysis`

2. After that, start the analysis process with the command below:

`docker-compose run --remove-orphans analysis python3 app.py [-h] --profiles-folder PROFILES_FOLDER [--ref-folder REF_FOLDER] [--log-detail-level {0,1,2}]`

## Executing without Docker

To run the application without Docker, you need to have Python3 and pip3 installed. Note: you may need to perform the following steps as root.

1. Execute the `bootstrap.sh` file to install dependencies for the analysis module:

`./analysis/bootstrap.sh`

2. Install the module dependencies with the following command (from the repository root):

`pip install -r ./analysis/requirements.txt`

3. Install DAMICORE dependencies with the following command (from the repository root):

`pip install -r ./analysis/damicore_requirements.txt`

4. Then, run the application:

`python3 app.py [-h] --profiles-folder PROFILES_FOLDER [--ref-folder REF_FOLDER] [--log-detail-level {0,1,2}]`

5. If, instead, you want to execute the module through the Flask API, run the following command:

`python3 -m flask run`

## Command-line example

Here is an execution example for running the analysis module with two arbitrary folders:

`python3 app.py --profiles-folder ../profiles/e55c9410-b953-45b8-bbe3-324ca6294fe7 --ref-folder ../profiles/a6b32106-2b72-424b-8516-19736c76b277`