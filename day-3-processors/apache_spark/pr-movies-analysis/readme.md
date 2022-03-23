https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html
https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html

### version and jars
```sh
# pyspark = v.3.1.1
# jars = /usr/local/lib/python3.9/site-packages/pyspark/jars
pyspark --version
```

### produce data into topics
```sh
# bash script ~ ingestion app
# src-app-users-json
# src-app-movies-titles-json

# retrieve topic info
k get kafkatopics
```

### retrieve data & verify transformations
```sh
# change interpreter to local ~ 3.9
# verify settings
# 1 = batch
# 2 = stream

# kafka
BROKER=143.244.200.162:9094

kcat -C -b $BROKER -t src-app-users-json -J -o end
kcat -C -b $BROKER -t src-app-movies-titles-json -J -o end

kcat -C -b $BROKER -t output-pyspark-counts-country-batch-json -J -o start
kcat -C -b $BROKER -t output-pyspark-counts-genres-stream-json -J -o start
```