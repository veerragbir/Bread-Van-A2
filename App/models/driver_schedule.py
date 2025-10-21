from App.database import db
from datetime import datetime

# DriverSchedule model: stores driver runs for streets with start/end times
class DriverSchedule(db.Model):
    __tablename__ = "driver_schedule"   # so FK strings match

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    scheduled_start_time = db.Column(db.DateTime, nullable=False)
    scheduled_end_time = db.Column(db.DateTime, nullable=False)

    # Relationships
    driver = db.relationship("Driver", back_populates="schedules")
    stop_requests = db.relationship(
        "StopRequest",
        back_populates="schedule",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __init__(self, driver_id, street, scheduled_start_time, scheduled_end_time):
        self.driver_id = driver_id
        self.street = street
        self.scheduled_start_time = scheduled_start_time
        self.scheduled_end_time = scheduled_end_time

    def get_json(self):
        return {
            "id": self.id,
            "driver_id": self.driver_id,
            "street": self.street,
            "scheduled_start_time": self.scheduled_start_time.isoformat(),
            "scheduled_end_time": self.scheduled_end_time.isoformat()
        }
