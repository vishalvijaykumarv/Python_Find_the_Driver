from flask import Flask, request, render_template, jsonify
from datetime import datetime
from utilities import *

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('main.html')


@app.route('/next_que')
def next_que():
    return render_template('get_driver.html')


@app.route('/active_rides')
def active_rides():
    return render_template('rides_list.html')


@app.route('/free_drivers')
def free_drivers():
    return render_template('free_drivers.html')


@app.route('/get_free_drivers', methods=['GET'])
def get_free_drivers():
    return jsonify(get_drivers())


@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    connection = pymysql.connect(**config)
    try:
        if connection.open:
            return 'Database connection is established'
        else:
            return 'Database connection is not established'
    except pymysql.Error as error:
        return 'Error connecting to the database: {}'.format(error)
    finally:
        if connection and connection.open:
            connection.close()


@app.route('/driver_sign_up', methods=['POST'])
def create_driver():
    # for key, value in request.json.items():
    #     print(f'{key}: {value}')

    name = request.json.get('name')
    current_latitude = request.json.get('current_latitude')
    current_longitude = request.json.get('current_longitude')
    on_ride = request.json.get('on_ride')
    price_km = request.json.get('price_km')

    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Update values in the 'user_rides' table
            sql = """
                INSERT INTO uber_demo.driver_data (
                    name, current_latitude, current_longitude, on_ride, price_km
                )
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    current_latitude = VALUES(current_latitude),
                    current_longitude = VALUES(current_longitude),
                    on_ride = VALUES(on_ride),
                    price_km = VALUES(price_km)
            """

            values = (
                name, current_latitude, current_longitude, on_ride, price_km
            )
            print(sql)

            cursor.execute(sql, values)
            connection.commit()

        return 'Driver information updated successfully'
    except pymysql.Error as error:
        return 'Error updating Driver information: {}'.format(error)
    finally:
        if connection and connection.open:
            connection.close()


@app.route('/create_ride', methods=['POST'])
def update_user_ride():
    user_name = request.json.get('user_name')
    pickup_latitude = float(request.json.get('pickup_latitude'))
    pickup_longitude = float(request.json.get('pickup_longitude'))
    pickup_address = request.json.get('pickup_address')
    dropoff_latitude = float(request.json.get('dropoff_latitude'))
    dropoff_longitude = float(request.json.get('dropoff_longitude'))
    dropoff_address = request.json.get('dropoff_address')

    requested_time = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    travel_distance = calculate_distance(pickup_latitude, pickup_longitude,
                                         dropoff_latitude, dropoff_longitude)
    estimated_duration = calculate_estimated_time(travel_distance)
    on_ride = 0

    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Update values in the 'user_rides' table
            sql = """
                INSERT INTO uber_demo.user_rides (
                    user_name, requested_time, pickup_latitude, pickup_longitude, pickup_address,
                    dropoff_latitude, dropoff_longitude, dropoff_address, estimated_duration,on_ride
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
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

            values = (
                user_name, requested_time, pickup_latitude, pickup_longitude, pickup_address,
                dropoff_latitude, dropoff_longitude, dropoff_address, estimated_duration, on_ride
            )

            cursor.execute(sql, values)
            connection.commit()

        return 'User ride information updated successfully'
    except pymysql.Error as error:
        return 'Error updating user ride information: {}'.format(error)
    finally:
        if connection and connection.open:
            connection.close()


@app.route('/get_driver', methods=['GET'])
def find_best_driver():
    """
    --- get the user requested ride based on requested time from user_rides table ( pick the first_one )
    --- get available drivers list based on-ride = 0
    -- get pick location from the user_rides and check which driver is having less distance & lower price
    :return: the best driver json data
    """
    ride_in_que = dict(get_one_user_ride())
    available_drivers = get_active_drivers()
    pickup_latitude, pickup_longitude = ride_in_que.get('pickup_latitude'), ride_in_que.get('pickup_longitude')
    pickup_driver = get_less_distance_driver(pickup_latitude, pickup_longitude, available_drivers)
    output = {
        "rider_name": ride_in_que.get('user_name'),
        "pickup_location": (pickup_latitude, pickup_longitude),
        "drop_location": (ride_in_que.get('dropoff_latitude'), ride_in_que.get('dropoff_longitude')),
        "pickup_driver_name": pickup_driver.get('name'),
        "driver_location": (pickup_driver.get('current_latitude'), pickup_driver.get('current_longitude')),
        "price_per_km": pickup_driver.get('price_km'),
        "distance_from_rider": pickup_driver.get('distance')
    }
    return jsonify(output)
    # return render_template('get_driver.html')


@app.route('/start_drive', methods=['POST'])
def start_drive():
    """
    get the user & driver ( name / id ) from the input
    mark the user_rides from 0 to 1 ( which means the user got the driver )
    mark driver_data on_ride from 0 to 1  ( which means the driver got the user )
    :return:
    """
    rider_name = request.json.get('rider_name')
    driver_name = request.json.get('pickup_driver_name')
    connection = pymysql.connect(**config)
    print(rider_name, driver_name)
    with connection.cursor() as cursor:
        # Update values in the 'user_rides' table
        rider_name_update_sql = f"""
        UPDATE `user_rides` SET `driver_name` = '{driver_name}' , `on_ride` = 1 WHERE `user_rides`.`user_name` = '{rider_name}';
        """
        driver_name_update_sql = f"""
        UPDATE `driver_data` SET `on_ride` = 1 WHERE `driver_data`.`name` = '{driver_name}';
        """
        # print(rider_name_update_sql)
        # print(driver_name_update_sql)
        cursor.execute(rider_name_update_sql)
        cursor.execute(driver_name_update_sql)
        connection.commit()
    return f"{rider_name} & {driver_name} updated ride status into on_ride"


@app.route('/get_active_rides', methods=['GET'])
def get_rides():
    return jsonify(get_active_rides())


@app.route('/complete_ride', methods=['POST'])
def update_ride_status():
    rider_drop_lat, rider_drop_long = request.json.get('dropoff_latitude'), request.json.get('dropoff_longitude')
    driver_name = request.json.get('name')
    mark_complete(driver_name, rider_drop_lat, rider_drop_long)
    return f"{driver_name} info updated"


if __name__ == '__main__':
    app.run()
