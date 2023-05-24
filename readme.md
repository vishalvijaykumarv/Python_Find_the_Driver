# Uber Driver System Clone

This Flask app is a clone of the Uber driver system. It provides a set of APIs for managing drivers, rides, and their status. Below you will find the details of the available endpoints and their functionalities.

#### ```Python run_server.py```  for running the API server 
#### ```Python upload_dummy_data.py``` for uploading dummy data
#### please make sure that you configured the mysql db connection at ```config``` variable at ```utilities.py```

## Endpoints

### GET /check_db_connection

- **Description**: Returns the status of the database connection.

### GET /next_que

- **Description**: Displays the ride queue in the user interface (UI).

### GET /active_rides

- **Description**: Displays the list of active rides in the UI.

### GET /free_drivers

- **Description**: Shows the list of free drivers in the UI.

### GET /get_free_drivers

- **Description**: Retrieves all free drivers from the database.

### GET /get_active_rides

- **Description**: Retrieves the list of active rides from the database.

### GET /get_driver

- **Description**: Analyzes the database and retrieves a suitable driver.

### POST /driver_sign_up

- **Description**: Adds a new driver to the system with the provided inputs.

- **Sample JSON Input**:

```json
{
  "name": "Driver John",
  "current_latitude": "40.7181",
  "current_longitude": "-73.9647",
  "on_ride": 0,
  "price_km": "15.50"
}
```

### POST /create_ride
- **Description**: Creates a new ride and updates it in the database with the provided inputs.

- **Sample JSON Input**:
```json
{
  "user_name": "Alice Johnson",
  "pickup_latitude": "40.7128",
  "pickup_longitude": "-74.0060",
  "pickup_address": "123 Main St",
  "dropoff_latitude": "40.7489",
  "dropoff_longitude": "-73.9680",
  "dropoff_address": "456 Elm St"
}
```

### POST /start_drive
- **Description**: Marks the ride as started and completed. This API is called from the UI with inputs.

### POST /complete_ride
- **Description**: Marks the ride as completed and updates the driver's location. This API is called from the UI with inputs.

Note:-
Please ensure you have the necessary dependencies installed and the Flask app is running properly before using these APIs.