# import libraries
from marshmallow import Schema, fields


# create users schema
class UsersSchema(Schema):
    user_id = fields.Integer(required=True)
    uuid = fields.String(required=False)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    date_birth = fields.String(required=False)
    city = fields.String(required=False)
    country = fields.String(required=False)
    company_name = fields.String(required=False)
    job = fields.String(required=False)
    phone_number = fields.String(required=False)
    last_access_time = fields.String(required=False)
    time_zone = fields.String(required=False)
    dt_current_timestamp = fields.String(required=False)

    # meta
    class Meta:
        ordered = True