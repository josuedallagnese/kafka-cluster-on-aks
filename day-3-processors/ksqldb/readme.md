# KSQLDB ~ SQL Streaming for Apache Kafka

## install ksqldb
```sh
# use cluster
kubectx aks-owshq-event-stream

# create namespace
k create namespace processing

# install ksqldb yaml files
k apply -f day-3-processors/ksqldb/yamls/ -n processing

# get info
kubens processing
kgpw
```

### working with ksqldb
```sh
# access ksqldb server
KSQLDB=ksqldb-server-688bbb48b-rknt4
k exec $KSQLDB -n processing -i -t -- bash ksql

# set latest offset read
SET 'auto.offset.reset' = 'earliest';
SET 'auto.offset.reset' = 'latest';

# show info
SHOW TOPICS;
SHOW STREAMS;
SHOW TABLES;
SHOW QUERIES;
```

##### create streams from topics [avro]
```sh
# generate events using ingestion app
# verify schema registry
# verify load balancer
export KAFKA_SCHEMA_REGISTRY = "http://schema_registry_ip:8081"

# bash file = batch_ksqldb_events.bash
python3.9 cli.py 'strimzi-musics-avro'
python3.9 cli.py 'strimzi-credit-card-avro'
python3.9 cli.py 'strimzi-agent-avro'
python3.9 cli.py 'strimzi-users-avro'

```

### housekeeping
```sh
# drop enriched stream
SHOW QUERIES;
TERMINATE QUERY_ID;

# drop streams
DROP STREAM KSQL_STREAM_APP_AGENT_AVRO;                                
DROP STREAM KSQL_STREAM_APP_CREDIT_CARD_AVRO;                          
DROP STREAM KSQL_STREAM_APP_MUSICS_AVRO;                               
DROP STREAM KSQL_STREAM_APP_USERS_AVRO;                                
DROP STREAM KSQL_STREAM_MYSQL_COMMERCE_AVRO;                           
DROP STREAM KSQL_STREAM_MYSQL_DEVICE_AVRO;                             
DROP STREAM KSQL_STREAM_SQLSERVER_CREDIT_CARD_AVRO;                    
DROP STREAM KSQL_STREAM_SQLSERVER_SUBSCRIPTION_AVRO;                   
DROP STREAM OUTPUT_KSQLDB_STREAM_PR_CREDIT_CARD_COMMERCE_ANALYSIS_AVRO;

```

### dropping topics [kafka]
```sh
# drop kafka topics output
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic output-ksqldb-stream-pr-musics-analysis-avro
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic output-ksqldb-stream-pr-credit-card-commerce-analysis-avro

```
