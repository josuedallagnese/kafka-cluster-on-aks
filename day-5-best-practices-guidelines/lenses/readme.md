### lenses


##### Queries
```sql

-- app-users
select * from src-app-users-avro

-- app-agents
select * from src-app-agent-avro

-- sql-credit-card
select * from src-sqlserver-credit-card-avro

-- sql-subscription
select * from src-sqlserver-subscription-avro

-- join query
select CONCAT(u.first_name, ' ',u.last_name ) as full_name,
r.destination,
r.price,
r.cab_type
from src-app-users-json as u join src-app-rides-json as r
on u.user_id = r.user_id limit 10;

-- query join from sql processor
select * from output_st_app_join_users_agents_events

SELECT
j.email,
j.full_name,
j.job,
j.city,
cc.credit_card_number,
cc.credit_card_type
from output_join_users_agents_events as j join src-app-credit-card-avro as cc on j.user_id = cc.user_id


```

##### SQL processors

```sh

# object name = count_beer_style_stream
# count data from beer based on style

SET defaults.topic.autocreate=true;
SET enable.auto.commit=true;
SET auto.offset.reset='earliest';


INSERT INTO output_stream_lenses_processor_count_rides
SELECT STREAM
      count(cab_type),cab_type FROM src-app-rides-json
WINDOW BY TUMBLE 1d
GROUP BY cab_type
# create join app users and rides

SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=true;
SET auto.offset.reset='latest';

INSERT INTO output_st_lenses_app_join_users_rides_events
SELECT STREAM
CONCAT(u.first_name, ' ',u.last_name ) as full_name,
r.destination,
r.price,
r.cab_type
from src-app-users-json as u join src-app-rides-json as r
on u.user_id = r.user_id
WITHIN 1h



SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';

INSERT INTO output_st_lenses_app_join_users_agents_events
SELECT STREAM
a.email,
CONCAT(u.first_name, ' ',u.last_name ) as full_name,
job,
city

from src-app-users-avro as u join src-app-agent-avro as a on u.user_id = a.user_id
WITHIN 1h




### CTE

SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';

WITH usersStream AS (
  SELECT STREAM *
  FROM src-app-users-json
);

WITH agentStream AS (
  SELECT STREAM *
  FROM src-app-agent-json
);


WITH enrichedUsersWithAgentInfoStream AS (
  SELECT STREAM
      CONCAT(u.first_name, ' ',u.last_name ) as full_name
    , u.country
    , u.job
    , a.email
    , a.platform
  FROM usersStream AS u JOIN agentStream AS a
        ON u.user_id = a.user_id
  WITHIN 1h
);

INSERT INTO output_enrichedUsersWithAgentInfoStream
SELECT TABLE
  COUNT(country) AS qty_country
FROM enrichedUsersWithAgentInfoStream
GROUP BY platform;




```

## register application in lenses

```sh

curl -X POST \
  20.96.128.53/api/v1/apps/external \
  -H 'Content-Type: application/json' \
  -H 'X-Kafka-Lenses-Token: register:4122eebd-accd-4831-b2f9-7837c6145d3e' \
  -d '{
    "name": "read-users-events-json",
    "metadata": {
        "version": "1.0.0",
        "owner": "Lenses",
        "deployment": "local",
        "tags": [
            "consumer",
            "events",
            "app"
        ]
    },
    "input": [{"name": "src-app-users-json"}],
    "output": [],
    "runners": []
}'


curl -X POST \
  20.96.128.53/api/v1/apps/external \
  -H 'Content-Type: application/json' \
  -H 'X-Kafka-Lenses-Token: register:4122eebd-accd-4831-b2f9-7837c6145d3e' \
  -d '{
    "name": "python-data-store-events-json",
    "metadata": {
        "version": "1.0.0",
        "owner": "Lenses",
        "deployment": "Local",
        "tags": [
            "producer",
            "events",
            "app"
        ]
    },
    "input": [],
    "output": [{"name": "src-app-users-json"}],
    "runners": []
}'




curl -X POST \
  20.96.128.53/api/v1/apps/external \
  -H 'Content-Type: application/json' \
  -H 'X-Kafka-Lenses-Token: register:4122eebd-accd-4831-b2f9-7837c6145d3e' \
  -d '{
    "name": "python-data-store-events-json",
    "metadata": {
        "version": "1.0.0",
        "owner": "Lenses",
        "deployment": "Local",
        "tags": [
            "producer",
            "events",
            "app"
        ]
    },
    "input": [],
    "output": [{"name": "src-app-music-data"}],
    "runners": []
}'




curl -X POST \
  20.96.128.53/api/v1/apps/external \
  -H 'Content-Type: application/json' \
  -H 'X-Kafka-Lenses-Token: register:4122eebd-accd-4831-b2f9-7837c6145d3e' \
  -d '{
    "name": "read-users-events-json",
    "metadata": {
        "version": "1.0.0",
        "owner": "Lenses",
        "deployment": "K8s",
        "tags": [
            "producer",
            "events",
            "app"
        ]
    },
    "input": [],
    "output": [{"name": "src-app-users-json"}],
    "runners": []
}'


```
