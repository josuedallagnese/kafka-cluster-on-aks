# Configuração do Cluster Kafka no cluster AKS

## Passos:

1.  Criação do namespace

    ```
    kubectl create ns ingestion
    ```

2. Install kafka operator
    ```
    helm repo add strimzi https://strimzi.io/charts/
    helm install kafka strimzi/strimzi-kafka-operator --namespace ingestion --version 0.26.0
    ```

3. Configura o contexto do kubectl para o novo namespace criado
    ```
    kubectl config set-context --current --namespace=ingestion
    ```

4. Criar o secrect da conexão com os bancos de dados
    ```
    Alterar no arquivo o usuário e a senha da sua instância de postgresql antes de aplicá-lo.

    kubectl create secret generic postgresql-credentials --from-file=deployments/strimzi/kafka-connect/postgresql-credentials.properties --namespace ingestion
    ```

5. Configura e expoe as métricas do kafka que serão expostas
    ```
    kubectl apply -f deployments/strimzi/metrics/kafka-metrics-config.yaml
    kubectl apply -f deployments/strimzi/metrics/zookeeper-metrics-config.yaml
    kubectl apply -f deployments/strimzi/metrics/connect-metrics-config.yaml
    kubectl apply -f deployments/strimzi/metrics/cruise-control-metrics-config.yaml
    ```

6. Criação do broker do kafka:
    6.1. Versão ephemeral: sem disco - apenas para testes
    ```
    kubectl apply -f deployments/strimzi/broker/kafka-ephemeral.yaml -n ingestion
    ```

    6.2. Create Kafka jbod: com disco e resiliente
    ```
    kubectl apply -f deployments/strimzi/broker/kafka-jbod.yaml -n ingestion
    ```

7. Criação do Kafka connect:
    ```
    kubectl apply -f deployments/strimzi/kafka-connect/kafka-connect.yaml -n ingestion
    ```

8. Criação do Kafka registry
    ```
    helm install schema-registry deployments/strimzi/cp-schema-registry --namespace ingestion
    ```

    8.1. Exposição com IP público do Kafka registry
    ```
    kubectl apply -f deployments/strimzi/lb/svc-lb-schema-registry.yaml
    ```

9. Exposição kafka exporter internamente dentro do cluster para coleta de telemetria
    ```
    kubectl apply -f deployments/strimzi/lb/svc-lb-kafka-exporter.yaml
    ```

10. Instalação do Kafka Bridge
    ```
    kubectl apply -f deployments/strimzi/kafka-bridge/secret-tls-slcdigital.yml
    kubectl apply -f deployments/strimzi/kafka-bridge/kafka-bridge.yaml
    kubectl apply -f deployments/strimzi/kafka-bridge/kafka-bridge-ingress.yaml
    ```

# Kafka Connector

## Criar tópicos no Kafka via especificações yaml
```
kubectl apply -f deployments/strimzi/topics/topic-customers.yaml -n ingestion
```

## Criando configuração de ingestão do Kafka connector para os topicos criados acima
```
Alterar o arquivo e definir:
- connection.url: url jdbc
- query: query a ser aplicada
- topic.prefix: nome do topic a ser enviado os dados
- incrementing.column.name: coluna que irá ser usada para o controle incremental

kubectl apply -f deployments/strimzi/connectors/ingest-customers-json.yaml -n ingestion
```

# Desinstalação do Cluster Kafka no cluster AKS
    ```
    helm uninstall kafka --namespace ingestion
    kubectl delete ns ingestion
    ```