# import libraries
from marshmallow import Schema, fields


# create rides schema
class EnrichedRides(Schema):
    user_id = fields.Integer(required=True)
    gender = fields.String(required=True)
    car_type = fields.String(required=True)
    model_type = fields.String(required=True)
    country = fields.String(required=True)
    city = fields.String(required=True)
    distance_in_km = fields.String(required=True)
    final_price_real = fields.String(required=True)
    dynamic_fare = fields.Boolean(required=True)
    time_period = fields.String(required=True)
    event_time = fields.String(required=True)
    processing_time = fields.String(required=True)