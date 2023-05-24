import pandas as pd
import pymysql
from datetime import datetime
import random
from utilities import config, generate_random_estimated_time

connection = pymysql.connect(**config)

drivers_csv = pd.read_csv('dummy_data/drivers.csv', dtype=str)
rides_csv = pd.read_csv('dummy_data/rides.csv', dtype=str)


def execute_mysql(sql, values):
    cursor = connection.cursor()
    print(sql)
    cursor.execute(sql, values)
    connection.commit()


def upload_drivers(input_df):
    # name, current_latitude, current_longitude, on_ride, price_km
    for idx, one_row in input_df.iterrows():
        name = one_row.get('name')
        current_latitude = one_row.get('current_latitude')
        current_longitude = one_row.get('current_longitude')
        on_ride = 0
        price_km = one_row.get('price_km')
        driver_sql = """INSERT INTO uber_demo.driver_data 
        (name, current_latitude, current_longitude, on_ride, price_km)
        VALUES (%s, %s, %s, %s, %s)
        
        ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        current_latitude = VALUES(current_latitude),
        current_longitude = VALUES(current_longitude),
        on_ride = VALUES(on_ride),
        price_km = VALUES(price_km)
        """
        driver_values = (name, current_latitude, current_longitude, on_ride, price_km)
        execute_mysql(driver_sql, driver_values)


def upload_rides(input_df):
    # user_name, requested_time, pickup_latitude, pickup_longitude, pickup_address,
    # dropoff_latitude, dropoff_longitude, dropoff_address, estimated_duration, on_ride, driver_name
    for idx, one_row in input_df.iterrows():
        current_time = datetime.now()
        requested_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        estimated_duration = str(generate_random_estimated_time())
        on_ride = 0
        user_name = one_row.get('user_name')
        pickup_latitude = one_row.get('pickup_latitude')
        pickup_longitude = one_row.get('pickup_longitude')
        pickup_address = one_row.get('pickup_address')
        dropoff_latitude = one_row.get('dropoff_latitude')
        dropoff_longitude = one_row.get('dropoff_longitude')
        dropoff_address = one_row.get('dropoff_address')

        rides_sql = """INSERT INTO uber_demo.user_rides
        (user_name, requested_time, pickup_latitude, pickup_longitude, pickup_address,
        dropoff_latitude, dropoff_longitude, dropoff_address, estimated_duration, on_ride)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE
        user_name = VALUES(user_name),
        requested_time = VALUES(requested_time),
        pickup_latitude = VALUES(pickup_latitude),
        pickup_longitude = VALUES(pickup_longitude),
        pickup_address = VALUES(pickup_address),
        dropoff_latitude = VALUES(dropoff_latitude),
        dropoff_longitude = VALUES(dropoff_longitude),
        dropoff_address = VALUES(dropoff_address),
        estimated_duration = VALUES(estimated_duration),
        on_ride = VALUES(on_ride)
        """
        rides_values = (user_name, requested_time, pickup_latitude, pickup_longitude, pickup_address,
                        dropoff_latitude, dropoff_longitude, dropoff_address, estimated_duration, on_ride)
        print(rides_sql)
        execute_mysql(rides_sql, rides_values)


if __name__ == '__main__':
    upload_drivers(input_df=drivers_csv)
    upload_rides(input_df=rides_csv)
