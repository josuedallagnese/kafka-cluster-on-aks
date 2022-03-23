# import libraries
import json
import logging
import datetime
import pymongo
from currency_converter import CurrencyConverter
from src.app import app, get_input_topic_src_app_credit_card_json, output_enriched_transactions

# build connection string
# get data from collection
client = pymongo.MongoClient("mongodb://root:w2nyCRBZKj@137.184.242.53:27017/owshq?authSource=admin")
db = client["owshq"]
payment_collection = db["payments"]

# add logging capabilities
logger = logging.getLogger(__name__)


# python function to enhance and understand transactions
# applying data enrichment rules for credit card and transactions
def transform_transactions_events(events):

    # adding global variables
    global user_id, city, country, credit_card_type, currency_mode, gender, subscription_price, final_price_in_real, event_time, processing_time

    # mongodb info to retrieve data
    # get data from payments collection
    find_user_id = {'user_id': events.user_id}
    output_payments_columns = {'_id': 0, 'user_id': 1, 'city': 1, 'country': 1, 'credit_card_type': 1, 'currency_mode': 1, 'gender': 1, 'subscription_price': 1}
    get_payments_dt = payment_collection.find_one(find_user_id, output_payments_columns)

    # treat data if [not null]
    # retrieve data from dict
    if get_payments_dt is not None:
        user_id = events.user_id
        city = get_payments_dt['city']
        country = get_payments_dt['country']
        credit_card_type = get_payments_dt['credit_card_type']
        currency_mode = get_payments_dt['currency_mode']
        gender = get_payments_dt['gender']
        subscription_price = get_payments_dt['subscription_price'][1:]

        # format time based data
        # get event and processing time
        event_time = datetime.datetime.strptime(events.dt_current_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        processing_time = datetime.datetime.now()

        # convert currency to real
        currency_converter = CurrencyConverter()
        get_correct_currency_conversion = currency_converter.convert(subscription_price, 'USD', 'BRL')
        final_price_in_real = float(round(get_correct_currency_conversion, 2))

        # get providers from events
        # if clause to enrich data [case when]
        # recipe to reduce code
        provider_options = {
            "JCB 16 digit": "jcb",
            "JCB 15 digit": "jcb",
            "Diners Club / Carte Blanche": "diners_club",
            "VISA 13 digit": "visa",
            "VISA 16 digit": "visa",
            "VISA 19 digit": "visa",
            "Discover": "discover",
            "American Express": "amex",
            "Mastercard": "mastercard",
            "Maestro": "mastercard"
        }
        result_providers_translation = provider_options.get(events.provider)

        # cast data to convert to json
        # building dict
        dict_output_events = {
            "user_id": user_id,
            "gender": 'male' if gender == 'M' else 'female',
            "city": city,
            "country": country,
            "provider": result_providers_translation,
            "subscription_price_in_dolar": subscription_price,
            "final_price_in_real": final_price_in_real,
            "event_time": str(event_time),
            "processing_time": str(processing_time)
        }

        # return data in json to output into a kafka topic
        return json.dumps(dict_output_events).encode('utf-8')


# reading events from apache kafka topic
# using python function to perform transformations
# adding concurrency to start multiple instances of an agent [workers]
@app.agent(get_input_topic_src_app_credit_card_json, concurrency=5)
async def credit_card_transaction_events(events):
    async for event in events:
        transformed_transactions_credit_card = transform_transactions_events(event)

        # raw and enriched data
        print(event)
        print(transformed_transactions_credit_card)

        # build dictionary to show metrics
        # available in faust api
        get_monitor_dt = {
            "messages_received_by_topic": app.monitor.messages_received_by_topic,
            "messages_processed_in_secs": app.monitor.messages_s,
            "last_committed_offsets": app.monitor.tp_committed_offsets
        }
        print(get_monitor_dt)

        # apache kafka output service
        # output to a sink topic
        # does not show calls that are not matching
        if transformed_transactions_credit_card is not None:
            await output_enriched_transactions.send(value=transformed_transactions_credit_card)