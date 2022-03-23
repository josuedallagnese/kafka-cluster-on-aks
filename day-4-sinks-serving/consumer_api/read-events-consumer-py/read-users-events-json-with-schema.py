# import libraries
import json
from sch_users import Users
from marshmallow_users import UsersSchema
from confluent_kafka import DeserializingConsumer

if __name__ == '__main__':

    # topic to assign
    # read messages
    topic = "src-app-users-json"

    # consumer properties
    # additional configs can be added
    consumer_conf = {
        "bootstrap.servers": "52.251.13.1:9094",
        "group.id": "read-users-events-json-with-schema",
        "auto.offset.reset": "latest"
    }

    # consumer info & subscribe
    # init consumer
    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe([topic])

    # loop over
    while True:
        try:
            events = consumer.poll(0.1)

            if events is None:
                continue

            # print topic, partition, offset and value info
            # get type from kafka consumer api by default
            print(events.topic(), events.partition(), events.offset(), events.value())
            print(type(events.value()))

            # transform [bytes] into json to read data properly
            # print type of the new converted variable
            get_users_events = json.loads(events.value().decode('utf8'))
            print(type(get_users_events))

            # accessing python dictionary
            # print data
            user_id = get_users_events["user_id"]
            print(user_id)

            # call pre-defined schema
            # sch_users = way to schematize the output
            get_users_schema_info = Users().to_dict_events(json.loads(events.value().decode('utf8')))
            print(get_users_schema_info)
            print(type(get_users_schema_info))

            # best way to convert objects
            # using marshmallow library
            # used for - validate, deserialize and serialize types
            users_schema = UsersSchema()
            output_users_schema = users_schema.dump(json.loads(events.value().decode('utf8')))
            print(output_users_schema)
            print(type(output_users_schema))

            # marshmallow [features]
            # filtering [columns]
            filter_columns_users = UsersSchema(only=("user_id", "city", "country", "dt_current_timestamp"))
            print(filter_columns_users.dump(json.loads(events.value().decode('utf8'))))

        except KeyboardInterrupt:
            break

    # close loop
    consumer.close()

