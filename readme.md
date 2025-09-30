# Bread Van App - Flask MVC Backend

A Flask-based backend system for a bread van notification application structured in the Model View Controller pattern.

## Features

### Driver Functionality
- Schedule drives to specific streets with estimated arrival times
- Update real-time status (Scheduled, In Progress, Completed)
- Track current location during active drives

### Resident Functionality
- View scheduled drives for their street (inbox)
- Request stops for specific drives with optional notes
- Track driver status and location in real-time

## Dependencies
* Python3/pip3
* Packages listed in requirements.txt

## Installing Dependencies
```bash
pip install -r requirements.txt
Configuration Management
Configuration information is provided via environment variables or config files.

In Development
When running in development environment, the app uses default_config.py:

python
SQLALCHEMY_DATABASE_URI = "sqlite:///bread-van.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
In Production
When deploying to production, pass configuration via environment variables in your deployment platform.

Available Commands
Database Management
bash
python wsgi.py initdb
User Management
bash
python wsgi.py list-users
Driver Operations
bash
python wsgi.py schedule-drive <driver_id> <street> <scheduled_time>
python wsgi.py update-status <schedule_id> <status> [--location LOCATION]
Resident Operations
bash
python wsgi.py view-inbox <resident_id>
python wsgi.py request-stop <resident_id> <schedule_id> [--notes NOTES]
python wsgi.py driver-status <schedule_id>
Utility Commands
bash
python wsgi.py list-schedules
Running the Project
For development:

bash
flask run
For production using gunicorn:

bash
gunicorn wsgi:app
Initializing the Database
When connecting to a fresh database, run:

bash
python wsgi.py initdb
Database Migrations
If changes to models are made, migrate the database:

bash
flask db init
flask db migrate
flask db upgrade
Testing
Run all tests:

bash
pytest
Generate test coverage report:

bash
coverage report
coverage html
Sample Workflow
Initialize the database:

bash
python wsgi.py initdb
View sample users:

bash
python wsgi.py list-users
View resident's inbox:

bash
python wsgi.py view-inbox 2
Request a stop:

bash
python wsgi.py request-stop 2 1 --notes "Need whole wheat bread"
Update driver status:

bash
python wsgi.py update-status 1 in_progress --location "Corner of Main and 1st"
Check driver status:

bash
python wsgi.py driver-status 1
Project Structure
text
bread_van_app/
├── app/
│   ├── models/          # Database models
│   ├── controllers/     # Business logic
│   └── views/          # API endpoints
├── wsgi.py             # CLI entry point
├── config.py           # Configuration
└── requirements.txt    # Dependencies
Troubleshooting
Views 404ing
Ensure new views are imported and added to the views list in main.py.

Database Issues
If adding models, migrate the database or delete the database file and reinitialize.

Module Import Errors
Ensure you're in the correct directory and virtual environment is activated.

bash
pip install -r requirements.txt