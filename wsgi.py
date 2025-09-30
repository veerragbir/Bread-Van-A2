import warnings
import logging
import sys
import os

# Nuclear option - suppress ALL warnings
warnings.filterwarnings("ignore")

# Suppress specific loggers
logging.getLogger('pkg_resources').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
logging.getLogger('flask_sqlalchemy').setLevel(logging.ERROR)

# Suppress Flask-Admin warnings
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

import click, pytest
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.main import create_app
from App.models import User, Resident, Driver, UserType, StopRequest, StopRequestStatus, DriverSchedule
from App.controllers import (
    UserController, StopRequestController, ScheduleController
)
from App.controllers.location import LocationController
from datetime import datetime, timedelta

app = create_app()
migrate = get_migrate(app)

# Rest of your code remains exactly the same...

# Initialize database command
@app.cli.command("init", help="Creates and initializes the database with sample data")
def initialize():
    db.drop_all()
    db.create_all()
    
    # Create sample driver
    driver, message = UserController.create_user(
        UserType.DRIVER, 
        "driver_john", 
        "driverpass", 
        "john.driver@breadvan.com", 
        "John Driver",
        vehicle_type="Bread Van",
        license_plate="BREAD123"
    )
    print(f"Created driver: {message}")
    
    # Create sample resident
    resident, message = UserController.create_user(
        UserType.RESIDENT,
        "resident_jane",
        "residentpass",
        "jane.resident@example.com",
        "Jane Resident",
        home_address="123 Main Street"
    )
    print(f"Created resident: {message}")
    
    # Create sample schedule
    start_time = datetime.utcnow() + timedelta(hours=2)  # 2 hours from now
    end_time = start_time + timedelta(hours=4)
    
    schedule, message = ScheduleController.create_schedule(
        driver.id,
        "Main Street",
        start_time,
        end_time
    )
    print(f"Created schedule: {message}")
    
    # Update driver location
    LocationController.update_driver_location(driver.id, "Starting location - Depot")
    print("Database initialized with sample data!")
    print(f"Driver ID: {driver.id}, Resident ID: {resident.id}, Schedule ID: {schedule.id}")

'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create-resident", help="Creates a resident")
@click.argument("name")
@click.argument("email")
@click.argument("username")
@click.argument("password")
@click.argument("address")
def create_resident_command(name, email, username, password, address):
    user, message = UserController.create_user(
        UserType.RESIDENT, username, password, email, name, home_address=address
    )
    if user:
        print(f"Resident {user.name} created with ID {user.id}!")
    else:
        print(f"Error: {message}")

@user_cli.command("create-driver", help="Creates a driver")
@click.argument("name")
@click.argument("email")
@click.argument("username")
@click.argument("password")
@click.argument("vehicle_type")
@click.argument("license_plate")
def create_driver_command(name, email, username, password, vehicle_type, license_plate):
    user, message = UserController.create_user(
        UserType.DRIVER, username, password, email, name, 
        vehicle_type=vehicle_type, license_plate=license_plate
    )
    if user:
        print(f"Driver {user.name} created with ID {user.id}!")
    else:
        print(f"Error: {message}")

@user_cli.command("list", help="Lists users")
@click.argument("type", default="all")
def list_users_command(type):
    if type == "residents":
        users = UserController.get_all_residents()
        print("Residents:")
    elif type == "drivers":
        users = UserController.get_all_drivers()
        print("Drivers:")
    else:
        users = UserController.get_all_users()
        print("All Users:")
    
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Username: {user.username}, Email: {user.email}, Type: {user.user_type.value}")

app.cli.add_command(user_cli)

'''
Schedule Commands
'''
schedule_cli = AppGroup('schedule', help='Schedule commands')

@schedule_cli.command("create", help="Create a schedule")
@click.argument("driver_id", type=int)
@click.argument("street")
@click.argument("start_time")
@click.argument("end_time")
def create_schedule_command(driver_id, street, start_time, end_time):
    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
        
        schedule, message = ScheduleController.create_schedule(driver_id, street, start_dt, end_dt)
        if schedule:
            print(f"Schedule created with ID {schedule.id} for {street}")
            print(f"Start: {start_dt}, End: {end_dt}")
        else:
            print(f"Error: {message}")
    except ValueError:
        print("Error: Invalid datetime format. Use ISO format: YYYY-MM-DD HH:MM:SS")

@schedule_cli.command("view-street", help="View schedules for a street")
@click.argument("street")
def view_schedules_street_command(street):
    schedules = ScheduleController.get_schedules_for_street(street)
    if schedules:
        print(f"Schedules for {street}:")
        for schedule in schedules:
            driver = UserController.get_user_by_id(schedule.driver_id)
            driver_name = driver.name if driver else "Unknown"
            print(f"ID: {schedule.id}, Driver: {driver_name}, Start: {schedule.scheduled_start_time}, End: {schedule.scheduled_end_time}, Street: {schedule.street}")
    else:
        print(f"No schedules found for {street}")

@schedule_cli.command("view-driver", help="View schedules for a driver")
@click.argument("driver_id", type=int)
def view_schedules_driver_command(driver_id):
    schedules = ScheduleController.get_schedules_for_driver(driver_id)
    driver = UserController.get_user_by_id(driver_id)
    if schedules and driver:
        print(f"Schedules for driver {driver.name}:")
        for schedule in schedules:
            print(f"ID: {schedule.id}, Street: {schedule.street}, Start: {schedule.scheduled_start_time}, End: {schedule.scheduled_end_time}")
    else:
        print(f"No schedules found for driver ID {driver_id}")

app.cli.add_command(schedule_cli)

'''
Stop Request Commands
'''
stop_cli = AppGroup('stop', help='Stop request commands')

@stop_cli.command("request", help="Request a stop")
@click.argument("resident_id", type=int)
@click.argument("schedule_id", type=int)
def request_stop_command(resident_id, schedule_id):
    stop_request, message = StopRequestController.create_stop_request(resident_id, schedule_id)
    if stop_request:
        print(f"Stop request created with ID {stop_request.id}")
        print(f"Resident ID: {resident_id}, Schedule ID: {schedule_id}")
    else:
        print(f"Error: {message}")

@stop_cli.command("list-resident", help="List stop requests for a resident")
@click.argument("resident_id", type=int)
def list_stops_resident_command(resident_id):
    stop_requests = StopRequestController.get_stop_requests_by_resident(resident_id)
    resident = UserController.get_user_by_id(resident_id)
    if stop_requests and resident:
        print(f"Stop requests for resident {resident.name}:")
        for req in stop_requests:
            schedule = ScheduleController.get_schedule_by_id(req.schedule_id)
            street = schedule.street if schedule else "Unknown"
            print(f"ID: {req.id}, Schedule ID: {req.schedule_id}, Street: {street}, Status: {req.status.value}, Requested: {req.request_time}")
    else:
        print(f"No stop requests found for resident ID {resident_id}")

app.cli.add_command(stop_cli)

'''
Location Commands
'''
location_cli = AppGroup('location', help='Location commands')

@location_cli.command("update", help="Update driver location")
@click.argument("driver_id", type=int)
@click.argument("location")
def update_location_command(driver_id, location):
    driver, message = LocationController.update_driver_location(driver_id, location)
    if driver:
        print(f"Driver {driver.name} location updated to: {location}")
        print(f"Updated at: {driver.location_updated_at}")
    else:
        print(f"Error: {message}")

@location_cli.command("get", help="Get driver location")
@click.argument("driver_id", type=int)
def get_location_command(driver_id):
    location_data, message = LocationController.get_driver_location(driver_id)
    if location_data:
        print(f"Location for Driver {location_data['driver_name']}:")
        print(f"Driver ID: {location_data['driver_id']}")
        print(f"Driver Name: {location_data['driver_name']}")
        print(f"Current Location: {location_data['current_location'] or 'Not set'}")
        print(f"Location Updated: {location_data['location_updated_at'] or 'Never'}")
        print(f"Vehicle Type: {location_data['vehicle_type']}")
        print(f"License Plate: {location_data['license_plate']}")
    else:
        print(f"Error: {message}")

@location_cli.command("list-all", help="Get all driver locations")
def list_all_locations_command():
    from App.models import Driver
    drivers_with_locations = Driver.query.filter(Driver.current_location.isnot(None)).all()
    
    if drivers_with_locations:
        print("All Driver Locations:")
        for driver in drivers_with_locations:
            print(f"Driver ID: {driver.id}, Driver Name: {driver.name}, Current Location: {driver.current_location}, Last Updated: {driver.location_updated_at or 'Never'}, Vehicle Type: {driver.vehicle_type}")
    else:
        print("No driver locations found")

app.cli.add_command(location_cli)

'''
Test Commands
'''
test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)

if __name__ == '__main__':
    app.run(debug=True)