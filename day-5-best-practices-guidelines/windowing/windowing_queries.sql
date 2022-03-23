
--working with ksqldb

--access ksqldb server


KSQLDB=ksqldb-server-688bbb48b-w9h2q
k exec $KSQLDB -n processing -i -t -- bash ksql

--set latest offset read
SET 'auto.offset.reset' = 'earliest';
SET 'auto.offset.reset' = 'latest';

--show info
SHOW TOPICS;
SHOW STREAMS;
SHOW TABLES;
SHOW QUERIES;


CREATE OR REPLACE STREAM ksql_stream_app_users_avro WITH (KAFKA_TOPIC='src-app-users-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');

--******************--
-- HOPPING WINDOW
--based on time intervals
--SIZE = window duration & ADVANCE = hop interval
--All hopping windows have the same duration, but they might overlap, depending on the length of time specified in the ADVANCE BY property
--******************--

SELECT FIRST_NAME, LAST_NAME, COUNT(*) AS QTY_NAME FROM KSQL_STREAM_APP_USERS_AVRO
WINDOW HOPPING (SIZE 10 SECONDS, ADVANCE BY 5 SECONDS)
WHERE FIRST_NAME LIKE 'A%'
GROUP BY FIRST_NAME,LAST_NAME
EMIT CHANGES;

--******************--
-- TUMBLING WINDOW
--Tumbling windows are a special case of hopping windows, based on time interval as hopping window
--They model fixed-size, non-overlapping, gap-less windows.

--******************--

SELECT FIRST_NAME, LAST_NAME, COUNT(*) AS QTY_NAME FROM KSQL_STREAM_APP_USERS_AVRO
WINDOW TUMBLING (SIZE 1 MINUTE)
WHERE FIRST_NAME LIKE 'A%'
GROUP BY FIRST_NAME,LAST_NAME
EMIT CHANGES;


--******************--
-- SESSION WINDOW
--A session window aggregates records into a session, which represents a period of activity separated by a specified gap of inactivity, or "idleness"
--records with timestamps that occur within the inactivity gap of existing sessions are merged into the existing sessions

--Session windows are different from the other window types, because:
--ksqlDB tracks all session windows independently across keys, so windows of different keys typically have different start and end times.
--Session window durations vary. Even windows for the same key typically have different durations.

--******************--

SELECT FIRST_NAME, LAST_NAME, COUNT(*) AS QTY_NAME FROM KSQL_STREAM_APP_USERS_AVRO
WINDOW SESSION (60 SECONDS)
WHERE FIRST_NAME LIKE 'A%'
GROUP BY FIRST_NAME,LAST_NAME
EMIT CHANGES;
