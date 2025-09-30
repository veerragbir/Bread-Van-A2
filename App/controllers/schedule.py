from App.models import DriverSchedule
from App.database import db
from datetime import datetime

class ScheduleController:
    @staticmethod
    def create_schedule(driver_id, street, scheduled_start_time, scheduled_end_time):
        """Create a new driver schedule"""
        try:
            # Check if driver exists
            from App.controllers.user import UserController
            driver = UserController.get_user_by_id(driver_id)
            if not driver or driver.user_type.value != 'driver':
                return None, "Driver not found"
            
            schedule = DriverSchedule(driver_id, street, scheduled_start_time, scheduled_end_time)
            db.session.add(schedule)
            db.session.commit()
            return schedule, "Schedule created successfully"
            
        except Exception as e:
            db.session.rollback()
            return None, f"Error creating schedule: {str(e)}"

    @staticmethod
    def get_schedules_for_street(street_name):
        """Get all schedules for a specific street"""
        return DriverSchedule.query.filter(
            DriverSchedule.street.ilike(f'%{street_name}%')
        ).all()

    @staticmethod
    def get_schedules_for_driver(driver_id):
        """Get all schedules for a driver"""
        return DriverSchedule.query.filter_by(driver_id=driver_id).all()

    @staticmethod
    def get_upcoming_schedules():
        """Get all upcoming schedules"""
        return DriverSchedule.query.filter(
            DriverSchedule.scheduled_start_time >= datetime.utcnow()
        ).order_by(DriverSchedule.scheduled_start_time).all()

    @staticmethod
    def get_schedule_by_id(schedule_id):
        """Get schedule by ID"""
        return db.session.get(DriverSchedule, schedule_id)