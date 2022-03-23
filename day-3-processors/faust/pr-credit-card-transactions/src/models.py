# import libraries
from faust import Record


# schema of event [src-app-credit-card-json]
class CreditCardEvent(Record, serializer='json'):
    uuid: str
    user_id: int
    provider: str
    number: str
    expire_data: str
    security_code: str
    dt_current_timestamp: str
