# Bread Van App - Flask MVC Backend

A Flask-based backend system for a bread van notification application structured in the Model View Controller pattern.

## Features

### Driver Functionality
- Schedule drives to specific streets with estimated arrival times
- Update real-time status and location
- Manage driving schedules

### Resident Functionality
- View scheduled drives for their street
- Request stops for specific drives
- Track driver location and status

## Dependencies
* Python3/pip3
* Packages listed in requirements.txt

## Installing Dependencies
```bash
pip install -r requirements.txt
Available Commands
Database Initialization
bash
flask init
User Management
bash
# Create a resident
flask user create-resident "Name" "email@example.com" "username" "password" "address"

# Create a driver  
flask user create-driver "Name" "email@example.com" "username" "password" "vehicle_type" "license_plate"

# List users
flask user list [all|residents|drivers]
Schedule Management
bash
# Create a schedule
flask schedule create <driver_id> "street" "start_time" "end_time"

# View schedules for a street
flask schedule view-street "street_name"

# View schedules for a driver
flask schedule view-driver <driver_id>
Stop Request Management
bash
# Request a stop
flask stop request <resident_id> <schedule_id>

# List stop requests for a resident
flask stop list-resident <resident_id>
Location Management
bash
# Update driver location
flask location update <driver_id> "location_description"

# Get driver location
flask location get <driver_id>

# List all driver locations
flask location list-all
Testing
bash
# Run tests
flask test user [all|unit|int]
Running the Project
For development:

bash
flask run
For production using gunicorn:

bash
gunicorn wsgi:app
Database Migrations
If changes to models are made, migrate the database:

bash
flask db init
flask db migrate
flask db upgrade
Sample Workflow
Initialize the database with sample data:

bash
flask init
Create additional users:

bash
flask user create-resident "Jane Doe" "jane@example.com" "jane_doe" "password123" "456 Oak Street"
flask user create-driver "Mike Driver" "mike@breadvan.com" "mike_d" "driverpass" "Bread Van" "VAN123"
Create a schedule:

bash
flask schedule create 1 "Main Street" "2024-01-15 09:00:00" "2024-01-15 11:00:00"
Request a stop:

bash
flask stop request 2 1
Update driver location:

bash
flask location update 1 "Corner of Main Street and 1st Avenue"
Testing
Run all tests:

bash
pytest
Run specific test types:

bash
flask test user unit
flask test user int
flask test user all
Generate test coverage report:

bash
coverage report
coverage html
Project Structure
text
bread_van_app/
├── app/
│   ├── models/          # Database models (User, Driver, Resident, Schedule, StopRequest)
│   ├── controllers/     # Business logic
│   ├── views/          # API endpoints
│   └── database.py     # Database configuration
├── wsgi.py             # CLI entry point
├── config.py           # Configuration
└── requirements.txt    # Dependencies
Configuration
The application uses environment-based configuration. In development, it uses default settings. In production, configure via environment variables:

SQLALCHEMY_DATABASE_URI: Database connection string

SECRET_KEY: Application secret key

ENV: Environment (DEVELOPMENT/PRODUCTION)

Troubleshooting
Database Issues
If encountering database errors, reinitialize:

bash
flask init
Module Import Errors
Ensure dependencies are installed:

bash
pip install -r requirements.txt
Command Not Found
Ensure you're in the correct directory and virtual environment is activated.

Deployment
Deploy to platforms like Render or Heroku by setting the appropriate environment variables and using gunicorn as the production server.

For support or contributions, please refer to the project repository.