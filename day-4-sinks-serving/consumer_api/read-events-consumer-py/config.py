# common variables
bootstrap_servers = "52.251.13.1:9094"
schema_registry_url = "http://20.94.0.255:8081"
topic_users_avro = "src-app-users-avro"
topic_users_json = "src-app-users-json"
ysql = "postgresql://yugabyte:yugabyte@20.80.197.3:5433/owshq"


# consumer settings info
def consumer_settings_json():

    json = {
         'bootstrap.servers': bootstrap_servers,
         'auto.offset.reset': "earliest"
        }

    return dict(json)
