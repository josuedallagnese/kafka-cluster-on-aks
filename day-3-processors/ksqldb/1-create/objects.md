#### create objects in ksqldb

For interact with kafka topics using ksqldb is needed create objects stream or tables to make queries.
* ksqldb docs = https://ksqldb.io/

```sh

# access ksqldb server using k8s
KSQLDB=ksqldb-server-688bbb48b-rknt4
k exec $KSQLDB -n processing -i -t -- bash ksql

# set latest or earliest offset read
SET 'auto.offset.reset' = 'earliest';
SET 'auto.offset.reset' = 'latest';

# read events from TOPICS
PRINT 'src-app-musics-avro' FROM BEGINNING;
PRINT 'src-app-credit-card-avro' FROM BEGINNING;
PRINT 'src.mongodb.owshq.restaurant' FROM BEGINNING;
PRINT 'src.mongodb.owshq.stripe' FROM BEGINNING;
PRINT 'src-postgres-coffee-json' FROM BEGINNING;
PRINT 'src-mysql-computer-avro' FROM BEGINNING;
PRINT 'cdc-mysql.owshq.device' FROM BEGINNING;
PRINT 'cdc-mysql.owshq.commerce' FROM BEGINNING;
PRINT 'src-postgres-food-avro' FROM BEGINNING;
PRINT 'owshq.sqlserver.dbo.credit_card' FROM BEGINNING;
PRINT 'output-ksqldb-stream-pr-musics-analysis-avro' FROM BEGINNING;
PRINT 'output-ksqldb-stream-pr-credit-card-commerce-analysis-avro' FROM BEGINNING;

# avro streams applications
#CREATE OR REPLACE STREAM ksql_stream_app_musics_avro WITH (KAFKA_TOPIC='src-app-musics-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
#CREATE OR REPLACE STREAM ksql_stream_app_credit_card_avro WITH (KAFKA_TOPIC='src-app-credit-card-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
#CREATE OR REPLACE STREAM ksql_stream_app_agent_avro WITH (KAFKA_TOPIC='src-app-agent-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
#CREATE OR REPLACE STREAM ksql_stream_app_users_avro WITH (KAFKA_TOPIC='src-app-users-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');

# avro streams connect source

CREATE OR REPLACE STREAM ksql_stream_postgres_food_avro WITH (KAFKA_TOPIC='src-postgres-food-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');


CREATE OR REPLACE STREAM ksql_stream_mysql_computer_avro WITH (KAFKA_TOPIC='src-mysql-computer-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
CREATE OR REPLACE STREAM ksql_stream_sqlserver_credit_card_avro WITH (KAFKA_TOPIC='src-sqlserver-credit-card-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
CREATE OR REPLACE STREAM ksql_stream_mysql_device_avro WITH (KAFKA_TOPIC='cdc-mysql.owshq.device', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
CREATE OR REPLACE STREAM ksql_stream_mysql_commerce_avro WITH (KAFKA_TOPIC='cdc-mysql.owshq.commerce', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
CREATE OR REPLACE STREAM ksql_stream_mongo_stripe_avro WITH (KAFKA_TOPIC='src.mongodb.owshq.stripe', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO',WRAP_SINGLE_VALUE='false');
CREATE OR REPLACE STREAM ksql_stream_mongo_stripe_avro WITH (KAFKA_TOPIC='src.mongodb.owshq.stripe', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO',WRAP_SINGLE_VALUE='false');





# json streams connect source



CREATE OR REPLACE STREAM ksql_stream_postgres_coffee_json
(
"payload" STRUCT <"incr" int,
                  "id" int,
                  "uid" VARCHAR,
                  "blend_name" VARCHAR,
                  "origin" VARCHAR,
                  "variety" VARCHAR,
                  "notes" VARCHAR,
                  "intensifier" VARCHAR,
                  "user_id" int,
                  "dt_current_timestamp" VARCHAR,
                  "messagetopic" VARCHAR,
                  "messagesource" VARCHAR>
)
WITH (KAFKA_TOPIC='src-postgres-coffee-json', VALUE_FORMAT='JSON', KEY_FORMAT = 'JSON');


# create table with aggretation
CREATE OR REPLACE TABLE ksqldb_table_pr_count_bank_avro
WITH (KAFKA_TOPIC='ksqldb-table-pr-count-bank-avro', PARTITIONS=9, VALUE_FORMAT='AVRO')
AS
SELECT
      "BANK_NAME",
      count("BANK_NAME") AS BANK_NAME_COUNT
FROM KSQL_TABLE_SQLSERVER_BANK_AVRO
GROUP BY "BANK_NAME"
emit changes;

```
