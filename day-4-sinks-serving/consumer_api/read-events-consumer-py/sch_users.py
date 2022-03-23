class Users(object):

    @staticmethod
    def to_dict_events(json_event):

        return {
            "user_id": json_event["user_id"],
            "uuid": json_event["uuid"],
            "first_name": json_event["first_name"],
            "last_name": json_event["last_name"],
            "date_birth": str(json_event["date_birth"]),
            "city": json_event["city"],
            "country": json_event["country"],
            "company_name": json_event["company_name"],
            "job": json_event["job"],
            "phone_number": json_event["phone_number"],
            "last_access_time": json_event["last_access_time"],
            "time_zone": json_event["time_zone"],
            "dt_current_timestamp": str(json_event["dt_current_timestamp"])
        }