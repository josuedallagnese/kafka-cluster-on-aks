### Sink connector




### apply yaml files into k8s
```sh
# deploy yaml files

k apply -f day-4-sinks-serving/sinks/minio/sink-minio-src-postgres-food-avro.yaml -n ingestion
k apply -f day-4-sinks-serving/sinks/minio/sink-minio-output-pyspark-counts-country-batch-json.yaml -n ingestion
k apply -f day-4-sinks-serving/sinks/minio/sink-minio-output-pyspark-counts-genres-stream-json.yaml -n ingestion
k apply -f day-4-sinks-serving/sinks/yugabytedb/sink-yugabytedb-ysql-mysql-computer-avro.yaml -n ingestion
k apply -f day-4-sinks-serving/sinks/yugabytedb/sink-yugabytedb-ysql-postgres-coffee-json.yaml -n ingestion

```
