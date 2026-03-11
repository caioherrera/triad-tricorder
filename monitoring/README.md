[pt-BR]

# Monitoramento

## Introdução

Esta pasta contem os arquivos relativos ao módulo de monitoramento da ferramenta Tricorder. Este módulo é responsável por executar um artefato, realizar a leitura dos dados de consumo de recursos (CPU, RAM, etc...) a nível de processo e salvá-los em arquivos .CSV.

O módulo de monitoramento pode ser utilizado em conjunto com a ferramenta, onde funciona como uma API desenvolvida em Flask para receber requisições de monitoramento através do endpoint `[POST]] /api/monitor`. Neste tipo de execução, o módulo envia uma requisição para `[POST] <backend>/api/monitor/status` com um status de seu monitoramento após cada execução,e para `[POST] <backend>/api/monitor/result` ao final de uma etapa de monitoramento, com o resultado completo desta.

Além disso, o módulo de monitoramento também pode ser executado de forma *stand-alone*, sem depender dos outros módulos da ferramenta. Para este tipo de execução, siga as instruções abaixo.

## Parâmetros do módulo

Para uma execução *stand-alone*, os seguintes parâmetros são previstos:

- `--command-line`: Lista de strings formando um comando a ser executado pelo módulo para executar a aplicação. Obrigatório.
- `--executions`: Valor inteiro representando o número de execuções da aplicação. Opcional, com valor padrão em 10.
- `--sample-interval`: Valor decimal representando o intervalo de coleta das amostras de consumo de recursos (em segundos). Opcional, com valor padrão em 0,1s.
- `--sample-count`: Valor inteiro representando o número de amostras a serem coletadas. Opcional, com valor padrão em 30.
- `--reading-types`: Lista de strings indicando as métricas a serem coletadas. Opcional, com valor padrão ["cpu", "ram", "io_data", "io_bytes"].
- `--replicate-application-logs-to-stdout`: Flag booleana indicando se os logs da aplicação devem ser replicados à saída padrão (stdout). Verdadeiro se presente, falso se omitida.
- `--log-detail-level`: Valor inteiro no intervalo [0, 2] representando o nível de detalhamento dos logs, sendo 0 = nenhum log, 1 = poucos logs, 2 = todos os logs. Opcional, com valor padrão em 2.

## Build e execução com Docker

1. Caso se esteja utilizando Docker para execução do módulo, execute o seguinte comando na pasta raíz deste repositório para fazer o build do container:

`docker-compose build monitor`

2. Após isso, execute o monitoramento seguindo o comando abaixo:

`docker-compose run --remove-orphans monitor python3 app.py [-h] [--executions EXECUTIONS] [--sample-interval SAMPLE_INTERVAL] [--sample-count SAMPLE_COUNT] --command-line COMMAND_LINE [COMMAND_LINE ...] [--reading-types READING_TYPES [READING_TYPES ...]] [--replicate-application-logs-to-stdout] [--log-detail-level {0,1,2}]`

## Execução sem Docker

Para execução da aplicação sem Docker, é necessário possuir Python3 e pip3 instalado. Atenção: talvez você precise fazer os próximos passos com usuário root.

1. Instale as dependências através do seguinte comando (na pasta raíz do repositório):

`pip install -r ./monitoring/requirements.txt`

2. Além disso, verifique se a aplicação alvo requer passos específicos para sua instalação. No caso das aplicações **Decision Tree** e **Network Telemetry**, execute o arquivo `bootstrap.sh` equivalente:

`./monitoring/applications/decision_tree/bootstrap.sh`

3. Então, execute a aplicação:

`python3 app.py [-h] [--executions EXECUTIONS] [--sample-interval SAMPLE_INTERVAL] [--sample-count SAMPLE_COUNT] --command-line COMMAND_LINE [COMMAND_LINE ...] [--reading-types READING_TYPES [READING_TYPES ...]] [--replicate-application-logs-to-stdout] [--log-detail-level {0,1,2}]`

4. Caso queira utilizar o módulo por meio da API Flask, execute-o a partir do comando:

`python3 -m flask run`

## Exemplo de linha de comando

Abaixo um exemplo de execução para a aplicação **Decision Tree**, com a carga *iris haberman_survival*:

`python3 app.py --command_line python3 ./applications/decision_tree/dtc_experiment_code_API.py oil_spill mammography --repplicate-application-logs-to-stdout`

---

[en-US]

# Monitoring

## Introduction

This directory contains files related to the monitoring module for the Tricorder tool. This module is responsible for executing an artifact, reading data regarding its resource consumption (CPU, RAM, etc...) at process level
and saving the readings in a .CSV file.

The monitoring module can be used through the Tricorder tool, where it will work as a Flask API to receive monitoring requests through the endpoint `[POST]] /api/monitor`. In this execution setup, the module will send a request to `[POST] <backend>/api/monitor/status` with a monitoring status after each execution, and to `[POST] <backend>/api/monitor/result` at the end of the monitoring step, with the final result for the task.

Aside from that, the monitoring module can also be executed stand-alone, without relying on the tool and its modules. For this type of execution, follow the instructions below.

## Module parameters

For stand-alone execution, the following parameters are available:

- `--command-line`: List of strings forming a command to be executed by the module to run the application. Required.
- `--executions`: Integer value representing the number of times the application will be executed. Optional, default is 10.
- `--sample-interval`: Decimal value representing the interval between resource consumption samples (in seconds). Optional, default is 0.1s.
- `--sample-count`: Integer value representing the number of samples to be collected. Optional, default is 30.
- `--reading-types`: List of strings indicating which metrics will be collected. Optional, default is ["cpu", "ram", "io_data", "io_bytes"].
- `--replicate-application-logs-to-stdout`: Boolean flag indicating whether the application's logs should be replicated to standard output (stdout). True if present, false if omitted.
- `--log-detail-level`: Integer value in the range [0, 2] representing the log detail level, where 0 = no logs, 1 = minimal logs, 2 = all logs. Optional, default is 2.

## Building and executing with Docker

1. If you are using Docker to run the module, execute the following command in the root directory of this repository to build the container:

`docker-compose build monitor`

2. After that, start the monitoring process with the command below:

`docker-compose run --remove-orphans monitor python3 app.py [-h] [--executions EXECUTIONS] [--sample-interval SAMPLE_INTERVAL] [--sample-count SAMPLE_COUNT] --command-line COMMAND_LINE [COMMAND_LINE ...] [--reading-types READING_TYPES [READING_TYPES ...]] [--replicate-application-logs-to-stdout] [--log-detail-level {0,1,2}]`

## Executing without Docker

To run the application without Docker, you need to have Python3 and pip3 installed. Note: you may need to perform the following steps as root.

1. Install the dependencies with the following command (from the repository root):

`pip install -r ./monitoring/requirements.txt`

2. Also, check whether the target application requires specific steps to be installed. In the case of the applications **Decision Tree** e **Network Telemetry**, execute the corresponding `bootstrap.sh` file:

`./monitoring/applications/decision_tree/bootstrap.sh`

3. Then, run the application:

`python3 app.py [-h] [--executions EXECUTIONS] [--sample-interval SAMPLE_INTERVAL] [--sample-count SAMPLE_COUNT] --command-line COMMAND_LINE [COMMAND_LINE ...] [--reading-types READING_TYPES [READING_TYPES ...]] [--replicate-application-logs-to-stdout] [--log-detail-level {0,1,2}]`

4. If, instead, you want to execute the module through the Flask API, run the following command:

`python3 -m flask run`

## Command-line example

Here is an execution example for monitoring the application **Decision Tree**, with its workload *iris haberman_survival*:

`python3 app.py --command_line python3 ./applications/decision_tree/dtc_experiment_code_API.py oil_spill mammography --repplicate-application-logs-to-stdout`