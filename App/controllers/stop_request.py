from App.models import StopRequest, StopRequestStatus, DriverSchedule
from App.database import db
from datetime import datetime, timedelta

class StopRequestController:
    @staticmethod
    def create_stop_request(resident_id, schedule_id):
        """Create a stop request with business rule enforcement"""
        try:
            # Check if schedule exists
            schedule = db.session.get(DriverSchedule, schedule_id)
            if not schedule:
                return None, "Schedule not found"
            
            # Check if resident exists
            from App.controllers.user import UserController
            resident = UserController.get_user_by_id(resident_id)
            if not resident or resident.user_type.value != 'resident':
                return None, "Resident not found"
            
            # Business rule: Stop must be requested at least 1 hour before departure
            time_until_departure = schedule.scheduled_start_time - datetime.utcnow()
            if time_until_departure < timedelta(hours=1):
                return None, "Stop requests must be made at least 1 hour before departure"
            
            # Check if resident already has a request for this schedule
            existing_request = StopRequest.query.filter_by(
                resident_id=resident_id, 
                schedule_id=schedule_id
            ).first()
            
            if existing_request:
                return None, "Stop request already exists for this schedule"
            
            stop_request = StopRequest(resident_id, schedule_id)
            db.session.add(stop_request)
            db.session.commit()
            
            return stop_request, "Stop request created successfully"
            
        except Exception as e:
            db.session.rollback()
            return None, f"Error creating stop request: {str(e)}"

    @staticmethod
    def get_stop_requests_by_resident(resident_id):
        """Get all stop requests for a resident"""
        return StopRequest.query.filter_by(resident_id=resident_id).all()

    @staticmethod
    def get_stop_requests_by_schedule(schedule_id):
        """Get all stop requests for a schedule"""
        return StopRequest.query.filter_by(schedule_id=schedule_id).all()

    @staticmethod
    def update_stop_request_status(request_id, status):
        """Update stop request status"""
        try:
            stop_request = db.session.get(StopRequest, request_id)
            if not stop_request:
                return None, "Stop request not found"
            
            stop_request.status = status
            db.session.commit()
            return stop_request, "Stop request status updated successfully"
            
        except Exception as e:
            db.session.rollback()
            return None, f"Error updating stop request: {str(e)}"