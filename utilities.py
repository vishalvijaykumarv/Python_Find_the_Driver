from math import radians, sin, cos, sqrt, atan2
from math import dist
import pymysql
import random

config = dict(host='localhost', user='root', password='password', db='uber_demo', charset='utf8mb4',
              cursorclass=pymysql.cursors.DictCursor)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude values to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Calculate the differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply the Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance in kilometers
    distance = R * c

    return distance


def calculate_estimated_time(distance):
    total_seconds = distance * 60  # Convert distance to seconds
    # Convert total seconds to hours, minutes, and seconds
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    # Format the time as "hh:mm:ss"
    formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return formatted_time


def get_less_distance_driver(pickup_latitude, pickup_longitude, drivers_list):
    temp_list = []
    for one_driver in drivers_list:
        current_latitude = float(one_driver.get('current_latitude'))
        current_longitude = float(one_driver.get('current_longitude'))
        distance = calculate_distance(current_latitude, current_longitude, float(pickup_latitude),
                                      float(pickup_longitude))
        one_driver['distance'] = str(distance)
        temp_list.append(one_driver)

    best_driver = min(temp_list, key=lambda driver: (float(driver['distance']), float(driver['price_km'])))
    return best_driver


def get_one_user_ride():
    """
    SELECT * FROM `user_rides` WHERE on_ride = 0 ORDER BY `user_rides`.`requested_time` ASC
    :return: return latest ride from the db
    """
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql = "SELECT * FROM `user_rides` WHERE on_ride = 0 ORDER BY `user_rides`.`requested_time` ASC"
    cursor.execute(sql)
    first_row = cursor.fetchone()
    cursor.close()
    connection.close()
    return first_row


def get_active_drivers():
    """
    SELECT * FROM `driver_data` WHERE on_ride = 0;
    :return: driver list
    """
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql = "SELECT * FROM `driver_data` WHERE on_ride = 0 ORDER BY `driver_data`.`price_km` ASC;"
    cursor.execute(sql)
    drivers_dict_list = cursor.fetchall()
    cursor.close()
    connection.close()
    return drivers_dict_list


def get_active_rides():
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    get_rides_sql = f""" SELECT driver_data.name,
    user_rides.user_name,
    user_rides.requested_time,
    user_rides.pickup_latitude,
    user_rides.pickup_longitude,
    user_rides.pickup_address,
    user_rides.dropoff_latitude,
    user_rides.dropoff_longitude,
    user_rides.dropoff_address, 
    user_rides.estimated_duration
    FROM user_rides INNER JOIN driver_data ON driver_data.name = user_rides.driver_name 
    WHERE user_rides.on_ride = 1 and driver_data.on_ride = 1;"""
    cursor.execute(get_rides_sql)
    drivers_dict_list = cursor.fetchall()
    output_data = [{**item, 'requested_time': item['requested_time'].strftime("%Y-%m-%d %H:%M:%S"),
                    'estimated_duration': str(
                        item['estimated_duration'])} if 'requested_time' in item and 'estimated_duration' in item
                   else item for item in drivers_dict_list]

    cursor.close()
    connection.close()
    # print(output_data)
    return output_data


def mark_complete(driver_name, rider_drop_lat, rider_drop_long):
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    driver_status_update_sql = f"""
     UPDATE `driver_data` SET
     `current_latitude` = '{rider_drop_lat}',
     `current_longitude` = '{rider_drop_long}',
     `on_ride` = '0'
     WHERE `name` = '{driver_name}';
     """
    cursor.execute(driver_status_update_sql)
    connection.commit()
    print(driver_status_update_sql)
    print(driver_name, rider_drop_lat, rider_drop_long)
    return driver_status_update_sql


def get_drivers():
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    get_drivers_sql = f"""
    SELECT name,price_km FROM `driver_data` WHERE `on_ride` = 0
     """
    cursor.execute(get_drivers_sql)
    drivers_dict_list = cursor.fetchall()
    print(drivers_dict_list)
    return drivers_dict_list


def generate_random_estimated_time():
    hours = 0
    minutes = random.randint(5, 10)
    seconds = 0
    # Format the time as "hh:mm:ss"
    formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return formatted_time

