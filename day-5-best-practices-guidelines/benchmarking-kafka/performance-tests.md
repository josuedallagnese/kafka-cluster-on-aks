# Performance Tests [Strimzi]

https://gist.github.com/ueokande/b96eadd798fff852551b80962862bfb3  
https://gist.github.com/dongjinleekr/d24e3d0c7f92ac0f80c87218f1f5a02b  
https://blog.clairvoyantsoft.com/benchmarking-kafka-e7b7c289257d  
https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines

### strimzi
```sh
# get kafka info
k get strimzi
k get kafka
k get kafkatopics
k get kafkarebalance
```

### kafka connect & connectors
```sh
# get connect & connector
k get kafkaconnect -o yaml
k get kafkaconnectors
```

### test-cases
```sh
# grafana

# list topics
k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --list


####################################
# kafka-producer-perf-test.sh
# topic name = producer-test-strimzi-dev-acks-0
# partitions = 9
# replication factor = 3
# acks = 0
####################################

k exec -ti edh-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 2 --partitions 16 --topic producer-test-strimzi-dev-acks-0

k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic pproducer-test-strimzi-dev-acks-0 \
--num-records 2000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=0 \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196


k exec edh-kafka-1 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic pproducer-test-strimzi-dev-acks-1 \
--num-records 2000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=0 \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196


k exec edh-kafka-1 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic pproducer-test-strimzi-dev-acks-1 \
--num-records 2000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=0 \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196


k exec edh-kafka-1 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic producer-test-strimzi-dev-acks-0 \
--num-records 1000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=0 \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196

k exec edh-kafka-2 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic producer-test-strimzi-dev-acks-0 \
--num-records 1000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=0 \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196

####################################
# kafka-producer-perf-test.sh
# topic name = producer-test-strimzi-dev-acks-1
# partitions = 9
# replication factor = 3
# acks = 1
####################################

k exec -ti edh-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 2 --partitions 32 --topic producer-test-strimzi-dev-acks-1


k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic producer-test-strimzi-dev-acks-1 \
--num-records 3000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=1 \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196

k exec edh-kafka-1 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic producer-test-strimzi-dev-acks-1 \
--num-records 3000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=1 \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196

k exec edh-kafka-2 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic producer-test-strimzi-dev-acks-1 \
--num-records 1000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=1 \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196

####################################
# kafka-producer-perf-test.sh
# topic name = producer-test-strimzi-dev-acks-all
# partitions = 9
# replication factor = 3
# acks = all
####################################

k exec -ti edh-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 2 --partitions 32 --topic producer-test-strimzi-dev-acks-0


k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic producer-test-strimzi-dev-acks-all \
--num-records 1000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=all \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196

k exec edh-kafka-1 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic producer-test-strimzi-dev-acks-all \
--num-records 1000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=all \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196

k exec edh-kafka-2 -c kafka -i -t -- bin/kafka-producer-perf-test.sh \
--topic producer-test-strimzi-dev-acks-all \
--num-records 1000000 \
--record-size 100 \
--throughput -1 \
--producer-props acks=all \
bootstrap.servers=localhost:9092 \
buffer.memory=67108864 \
batch.size=8196

######################
## kafka-consumer-perf-test.sh
######################

k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-consumer-perf-test.sh \
--bootstrap-server localhost:9092 \
--messages 1000000 \
--topic producer-test-strimzi-dev-acks-all \
--threads 1

k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-consumer-perf-test.sh \
--bootstrap-server localhost:9092 \
--messages 1000000 \
--topic producer-test-strimzi-dev-acks-all \
--threads 3

# read consumers [consumer groups]
k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group ? --describe
```
