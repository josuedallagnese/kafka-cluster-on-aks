--******************--
-- create stream output object stream with enriched events
--******************--

CREATE OR REPLACE STREAM output_ksqldb_stream_pr_credit_card_commerce_analysis_avro
WITH (KAFKA_TOPIC='output-ksqldb-stream-pr-credit-card-commerce-analysis-avro', PARTITIONS=16, VALUE_FORMAT='AVRO')
AS
SELECT
commerce."ROWKEY",
commerce."PRICE" as "PRICE",
commerce."PRICE_STRING" as "PRICE_STRING",
commerce."PROMO_CODE" as "PROMO_CODE",
commerce."USER_ID" as "USER_ID_COMMERCE",
commerce."DT_CURRENT_TIMESTAMP" as "DT_CURRENT_TIMESTAMP_COMMERCE",
card."CREDIT_CARD_NUMBER",
card."CREDIT_CARD_TYPE"
FROM KSQL_STREAM_MYSQL_COMMERCE_AVRO commerce
INNER JOIN KSQL_STREAM_SQLSERVER_CREDIT_CARD_AVRO card WITHIN 1 DAY
ON commerce."USER_ID" = card."USER_ID"
PARTITION BY commerce."ROWKEY"
emit changes;

--******************--
-- create table output object aggregation events
--******************--


CREATE OR REPLACE TABLE ksqldb_tb_pr_credit_card_type_analysis_avro
WITH (KAFKA_TOPIC='ksqldb-tb-pr-credit-card-type-analysis-avro', PARTITIONS=9, VALUE_FORMAT='AVRO')
AS
SELECT
      CREDIT_CARD_TYPE,
      count(CREDIT_CARD_TYPE) AS CREDIT_CARD_TYPE_COUNT
FROM KSQL_STREAM_SQLSERVER_CREDIT_CARD_AVRO
GROUP BY CREDIT_CARD_TYPE
EMIT CHANGES;
