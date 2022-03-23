# import libraries
import pandas as pd
import config
from sqlalchemy import create_engine

# pandas config
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# init class
class RidesTransformBatch:

    @staticmethod
    def rides_analysis(get_enriched_rides_dt):

        # convert list to dict
        # get and select needed columns
        # group by data
        get_rides_dt = pd.DataFrame(get_enriched_rides_dt, columns=['car_type', 'country', 'model_type', 'date'])
        get_columns = get_rides_dt[["car_type", "country", "model_type", 'date']]
        group_dt = get_columns.groupby(["car_type", "country", 'model_type', 'date']).size().reset_index(name='amount')

        # creating connection to database
        # set up sqlalchemy connection
        # insert pandas dataframe into table (replace if exists)
        cs_ysql = config.ysql
        ysql_engine = create_engine(cs_ysql)
        group_dt.to_sql('rides_per_country', ysql_engine, if_exists='replace', index=False, chunksize=100)

        # return pandas dataframe
        return group_dt



