from App.database import db
from datetime import datetime
from enum import Enum

# Status enum for stop requests
class StopRequestStatus(Enum):
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    COMPLETED = "completed"

class StopRequest(db.Model):
    __tablename__ = "stop_request"   # so FK strings match

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("driver_schedule.id"), nullable=False)
    request_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(StopRequestStatus), nullable=False, default=StopRequestStatus.REQUESTED)

    # Relationships
    resident = db.relationship("Resident", back_populates="stop_requests", foreign_keys=[resident_id])
    schedule = db.relationship("DriverSchedule", back_populates="stop_requests")

    def __init__(self, resident_id, schedule_id):
        self.resident_id = resident_id
        self.schedule_id = schedule_id
        self.request_time = datetime.utcnow()
        self.status = StopRequestStatus.REQUESTED

    def get_json(self):
        return {
            "id": self.id,
            "resident_id": self.resident_id,
            "schedule_id": self.schedule_id,
            "request_time": self.request_time.isoformat(),
            "status": self.status.value
        }
