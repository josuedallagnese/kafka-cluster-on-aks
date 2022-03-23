```shell
https://github.com/confluentinc/confluent-kafka-python
https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#
https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
https://marshmallow.readthedocs.io/en/stable/
```

```shell
# list topics
kubectl exec -ti edh-zookeeper-0 -- bin/kafka-topics.sh --list --zookeeper localhost:12181

# get topic info
k describe kafkatopic src-app-users-json

# read latest written offset per topic
kubectl exec -it edh-kafka-0 -- bash bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --time -1 --topic src-app-users-json

# read latest consumer info
kcat -C -b 52.251.13.1:9094 -t __consumer_offsets -J -o start
```

```shell
# get info from topic
# partitions = 3
k describe kafkatopic src-app-users-json

# scale consumer application
python3.9 s-read-users-events-json.py
python3.9 s-read-users-events-json.py
python3.9 s-read-users-events-json.py 
```

```shell
# verify config.py
# produce events
python3.9 cli.py 'strimzi-users-json'
python3.9 cli.py 'strimzi-users-avro'

# kafka consumer applications
s-read-users-events-json.py
read-users-events-json-with-schema.py & sch_users.py & marshmallow_users.py
read-events-avro.py
bc-analyze-rides-batch.py & fn_rides_analysis_batch.py
```

```shell
# verify partitions
# [6]
k describe kafkatopic src-app-users-json

# ingest data using ingestion app
# batch_users.bash
python3.9 cli.py 'strimzi-users-json'
python3.9 cli.py 'strimzi-users-avro'

# /Users/luanmorenomaciel/BitBucket/apache-kafka/day-4-sinks-serving/consumer_api/read-events-consumer-py
python3.9 s-read-users-events-json.py

# add more instances of the same app
python3.9 s-read-users-events-json.py
python3.9 s-read-users-events-json.py
```