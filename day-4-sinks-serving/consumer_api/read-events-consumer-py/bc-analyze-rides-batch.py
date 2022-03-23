# import libraries
import json
import time
from datetime import datetime
from confluent_kafka.cimpl import KafkaException
from confluent_kafka import DeserializingConsumer
from fn_rides_analysis_batch import RidesTransformBatch

# init consumer application
if __name__ == '__main__':

    # topic to assign
    # read messages ~ enhanced topic from faust app
    topic = "output-faust-enriched-rides"

    # consumer properties
    # reading from the first offset
    # return all messages
    consumer_conf = {
        "bootstrap.servers": "52.251.13.1:9094",
        "group.id": "bc-analyze-rides-batch-py",
        "auto.offset.reset": "earliest",
        "isolation.level": "read_uncommitted",
        "enable.auto.commit": "False",
        "auto.commit.interval.ms": 60000000
    }

    # consumer info & subscribe
    # init consumer
    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe([topic])

    # duration of application execution
    # time to execute the job
    execution_time = 20
    timeout = time.time() + int(execution_time)

    # make dict available
    get_rides_per_country = []

    # loop over
    try:
        while timeout >= time.time():
            events = consumer.poll(0.1)

            if events is None:
                continue

            if events.error():
                raise KafkaException(events.error())

            else:
                # print topic, partition, offset and value info
                # get type from kafka consumer api by default
                print(events.topic(), events.partition(), events.offset(), events.value())
                print(type(events.value()))

                # append data into a dictionary
                # save every event in a new dict
                # convert to json = [py dict].value().decode('utf8')
                get_kafka_values_dt = json.loads(events)
                print(get_kafka_values_dt)

                # create output dictionary
                # extract correct date from processing time
                date_rides = get_kafka_values_dt["processing_time"]
                extract_date_rides = datetime.strptime(date_rides, '%Y-%m-%d %H:%M:%S.%f')

                # filling dict to access outside of the loop
                dict_values_dt = {
                    "car_type": get_kafka_values_dt["car_type"],
                    "model_type": get_kafka_values_dt["model_type"],
                    "country": get_kafka_values_dt["country"],
                    "date": extract_date_rides.date()}

                # appending into the dictionary
                # get_rides_per_country
                get_rides_per_country.append(dict_values_dt)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

    # close loop
    consumer.close()

    # process data in batch using consumer app
    # fn_rides_analysis_batch = invoke python function to [enrich] data
    # group data and insert into database for analysis ~ tb = [rides_per_country]
    print(get_rides_per_country)
    output_enriched_dt = RidesTransformBatch.rides_analysis(get_rides_per_country)
    print(output_enriched_dt)




