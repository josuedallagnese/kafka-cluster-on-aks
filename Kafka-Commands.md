# Comandos

## Criar topico usando compactação
### log compaction
```shell
# creating a topic with cleanup policy equals to compact to enable log compaction,
# the default is delete which will delete old segments when their retention time and size limit has been reached
# delete.retention.ms = The amount of time to retain delete tombstone markers for log compacted topics
# segment.ms = This configuration controls the period of time after which kafka will force the log to roll even if
# the segment file isn't full to ensure that retention can delete or compact old data
# min.cleanable.dirty.ratio = is configuration controls how frequently the log compactor will attempt to clean the log
k exec -ti edh-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tp-log-compaction-json --config "cleanup.policy=compact" --config "delete.retention.ms=100" --config "segment.ms=100" --config "min.cleanable.dirty.ratio=0.01"

## Criar raw topic
kubectl exec -ti edh-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tp-log-compaction-alter-json

# Alterar topico existente
k exec -ti edh-kafka-0 -i -t -- bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name tp-log-compaction-alter-json --alter --add-config "cleanup.policy=compact"
k exec -ti edh-kafka-0 -i -t -- bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name tp-log-compaction-alter-json --alter --add-config "min.cleanable.dirty.ratio=0.01"
k exec -ti edh-kafka-0 -i -t -- bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name tp-log-compaction-alter-json --alter --add-config "delete.retention.ms=100"
k exec -ti edh-kafka-0 -i -t -- bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name tp-log-compaction-alter-json --alter --add-config "segment.ms=100"


## Listar todos os topicos
```
kubectl exec -ti edh-zookeeper-0 -- bin/kafka-topics.sh --list --zookeeper localhost:12181

kubectl exec -ti edh-zookeeper-0 -- bin/kafka-topics.sh --describe --zookeeper localhost:12181

```

## Listar um único tópico:
```
kubectl exec -ti edh-zookeeper-0 -- bin/kafka-topics.sh --describe --zookeeper localhost:12181 --topic customers
```

## Deletar um tópico:
Para deletar um topico é necessário que ele esteja configurado para isso.
Por padrão a exclusão de tópicos no kafka é desativada.
A nível de broker essa opção foi habilitada usando a propriedade: 'delete.topic.enable: true'.
Ver em deployments/strimzi/broker/kafka-jbod.yaml
```
kubectl exec -ti edh-zookeeper-0 -- bin/kafka-topics.sh --delete --topic customers --zookeeper localhost:12181
```

## Contar quantas mensagens existem em um topicos e em suas partições
```
kubectl exec -ti edh-zookeeper-0 -- bin/kafka-run-class.sh kafka.tools.GetOffsetShell --topic customers --time -1 --broker-list edh-kafka-bootstrap:9092
```

## Consumir dados de um tópico:
```
kubectl exec -ti edh-zookeeper-0 -- bin/kafka-console-consumer.sh --bootstrap-server edh-kafka-bootstrap:9092 --topic customers --from-beginning --max-messages 10
```

## Consultar os connectores cadastrados
### Via API - Para isso, precisa entrar dentro de um pod no cluster
```
curl -X GET edh-connect-api:8083/connectors
curl -X GET edh-connect-api:8083/connectors/customers

curl -X DELETE edh-connect-api:8083/connectors/customers
```

### Via kubectl
```
kubectl get kafkaconnectors -n ingestion
```

## Alterar a configuração de um topico após sua criação
### Via kafka configs - Alterando tempo de retenção para 7 dias:
```
kubectl exec -ti edh-zookeeper-0 -- bin/kafka-configs.sh --bootstrap-server 20.85.99.150:9094 --alter --entity-type topics --entity-name customers --add-config retention.ms=604800000604800000
```

### Alterando via yaml file.
Alterar o arquivo: deployments/strimzi/topics/topic-customers.yaml 
E aplicá-lo novamente usando o kubectl:

```
kubectl apply -f deployments/strimzi/topics/topic-customers.yaml -n ingestion
```

Verificar a configuração aplicada:

```
kubectl describe kafkaconnector customers -n ingestion
```

## Kafka-Bridge
https://ingestion-dev.your-domain.com.br

## Obter IP externo do Kafka External Bootstrap - via kubectl

```
kubectl get services -n ingestion edh-kafka-external-bootstrap --output jsonpath='{.status.loadBalancer.ingress[0].ip}'
```