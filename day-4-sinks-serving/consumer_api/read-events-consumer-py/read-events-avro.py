# import libraries
from config import bootstrap_servers, topic_users_avro, schema_registry_url
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError


# create class to encapsulate logic
# schema being consumer from schema registry
# apache avro format
class KafkaUsersEventAvro:

    # set up consumer info
    c = AvroConsumer({
        # kafka broker address
        'bootstrap.servers': bootstrap_servers,
        # name of group (consumer group)
        'group.id': 'read-users-events-avro-with-schema-registry',
        # schema registry location
        'schema.registry.url': schema_registry_url}
    )

    # subscribe to the topic
    c.subscribe([topic_users_avro])

    # while loop to read messages
    while True:
        try:
            # get data from kafka & handles
            # coordination, partition rebalance, heartbeats and fetching
            # interval in ms that will wait to pull data from broker
            msg = c.poll(10)

        # except if serialization fails
        except SerializerError as e:
            print("message deserialization failed for {}: {}".format(msg, e))
            break

        # if a message is successfully read move
        if msg is None:
            continue

        # if a error occurs
        if msg.error():
            print("avro consumer error: {}".format(msg.error()))
            continue

        print(msg.topic(), msg.partition(), msg.offset(), msg.key(), msg.value())

    # close loop
    c.close()


# main
if __name__ == '__main__':

    # read messages
    KafkaUsersEventAvro()