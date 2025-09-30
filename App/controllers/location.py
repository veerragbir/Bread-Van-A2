from App.models import Driver
from App.database import db
from datetime import datetime

class LocationController:
    @staticmethod
    def update_driver_location(driver_id, location_string):
        """Update driver's current location"""
        try:
            driver = db.session.get(Driver, driver_id)
            if not driver:
                return None, "Driver not found"
            
            driver.current_location = location_string
            driver.location_updated_at = datetime.utcnow()
            db.session.commit()
            return driver, "Driver location updated successfully"
            
        except Exception as e:
            db.session.rollback()
            return None, f"Error updating driver location: {str(e)}"

    @staticmethod
    def get_driver_location(driver_id):
        """Get driver's current location"""
        driver = db.session.get(Driver, driver_id)
        if not driver:
            return None, "Driver not found"
        
        return {
            'driver_id': driver.id,
            'driver_name': driver.name,
            'current_location': driver.current_location,
            'location_updated_at': driver.location_updated_at.isoformat() if driver.location_updated_at else None,
            'vehicle_type': driver.vehicle_type,
            'license_plate': driver.license_plate
        }, "Location retrieved successfully"