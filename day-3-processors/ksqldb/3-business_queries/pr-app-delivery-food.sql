--******************--
-- create stream output object stream with enriched events
--******************--


CREATE OR REPLACE STREAM ksqldb_stream_postgres_coffee_json
WITH (KAFKA_TOPIC='ksqldb-stream-postgresql-coffee-json',VALUE_FORMAT='JSON')
AS
SELECT
coffee."payload"->"incr",
coffee."payload"->"blend_name" as "blend_name",
coffee."payload"->"origin" as "origin",
coffee."payload"->"user_id" as "user_id",
coffee."payload"->"dt_current_timestamp" as "dt_current_timestamp"
FROM KSQL_STREAM_POSTGRES_COFFEE_JSON coffee
PARTITION BY coffee."payload"->"incr"
emit changes;




CREATE OR REPLACE STREAM output_ksqldb_stream_pr_food_coffee_device_analysis_avro
WITH (KAFKA_TOPIC='output-ksqldb-stream-pr-food-coffee-device-analysis-avro', PARTITIONS=16, VALUE_FORMAT='AVRO')
AS
SELECT
device."ROWKEY"->"INCR" as "INCR",
device."AFTER"->"MODEL" as "model",
device."AFTER"->"PLATFORM" as "platform",
coffee."blend_name",
coffee."origin",
food."DISH",
food."DESCRIPTION",
food."INGREDIENT"
FROM KSQL_STREAM_MYSQL_DEVICE_AVRO device
INNER JOIN KSQL_STREAM_POSTGRES_FOOD_AVRO food WITHIN 7 DAY
ON device."ROWKEY"->"INCR" = food."INCR"
INNER JOIN KSQLDB_STREAM_POSTGRES_COFFEE_JSON coffee WITHIN 7 DAY
ON device."ROWKEY"->"INCR" = coffee."incr"
PARTITION BY device."ROWKEY"->"INCR"
emit changes;
