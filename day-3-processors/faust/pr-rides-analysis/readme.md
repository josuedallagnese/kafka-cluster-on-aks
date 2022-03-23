```shell
# verify kafka connectivity
export KAFKA_BOOTSTRAP_SERVER = "kafka://143.244.200.162:9094"

# generate data into topic
# use ingestion app ~ batch_rides.bash
export TOPIC_SRC_APP_RIDES_JSON = "src-app-rides-json"
python3.9 cli.py 'strimzi-rides-json'

# init python faust application
faust -A src.app worker -l info

# verify output topic
# kafka
BROKER=143.244.200.162:9094
kcat -C -b $BROKER -t output-faust-enriched-rides -J -o end
```