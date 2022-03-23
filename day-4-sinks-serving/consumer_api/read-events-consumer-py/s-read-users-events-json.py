# import libraries
from confluent_kafka import Consumer

# specify consumer parameters
# auto.offset.reset = read last available event
# based on group ip
c = Consumer({
    "bootstrap.servers": "52.251.13.1:9094",
    "group.id": "read-users-events-json",
    "auto.offset.reset": "latest"
})

# assign a topic to read
# raw topic = src-app-users-json
c.subscribe(['src-app-users-json'])

# loop over events
# thread safety = immutable state of a class
# shared state in a app using same thread to multiple readers
while True:

    # poll = interval in [ms] to pull events
    # timeout in seconds
    events = c.poll(0.1)

    if events is None:
        continue

    if events.error():
        continue

    # read events
    # expose offset and value = event sent to apache kafka
    print(events.topic(), events.partition(), events.offset(), events.value().decode('utf-8'))

# close call
# terminate consumer
c.close()
