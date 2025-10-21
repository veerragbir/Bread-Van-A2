from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from enum import Enum
from datetime import datetime


class UserType(Enum):
    RESIDENT = "resident"
    DRIVER = "driver"

# Base User model (joined-table inheritance)
class User(db.Model):
    __tablename__ = "user"   # base table name used by FKs elsewhere

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": user_type,
        "polymorphic_identity": "user"
    }

    def __init__(self, username, password, email, name, user_type):
        self.username = username
        self.set_password(password)
        self.email = email
        self.name = name
        # allow either enum or string
        if isinstance(user_type, UserType):
            self.user_type = user_type
        else:
            self.user_type = UserType(user_type)

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "user_type": self.user_type.value
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)



# Resident subclass
class Resident(User):
    __tablename__ = "resident"

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    home_address = db.Column(db.String(200), nullable=False)

    # Relationships
    stop_requests = db.relationship(
        "StopRequest",
        back_populates="resident",
        cascade="all, delete-orphan",
        lazy=True
    )

    __mapper_args__ = {
        "polymorphic_identity": UserType.RESIDENT
    }

    def __init__(self, username, password, email, name, home_address):
        super().__init__(username, password, email, name, UserType.RESIDENT)
        self.home_address = home_address

    def get_json(self):
        base = super().get_json()
        base.update({"home_address": self.home_address})
        return base



# Driver subclass
class Driver(User):
    __tablename__ = "driver"

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    vehicle_type = db.Column(db.String(100), nullable=False)
    license_plate = db.Column(db.String(20), nullable=False)
    current_status = db.Column(db.String(50), default="available")
    current_location = db.Column(db.String(200))
    location_updated_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    schedules = db.relationship(
        "DriverSchedule",
        back_populates="driver",
        cascade="all, delete-orphan",
        lazy=True
    )

    __mapper_args__ = {
        "polymorphic_identity": UserType.DRIVER
    }

    def __init__(self, username, password, email, name, vehicle_type, license_plate):
        super().__init__(username, password, email, name, UserType.DRIVER)
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate
        self.current_status = "available"

    def get_json(self):
        base = super().get_json()
        base.update({
            "vehicle_type": self.vehicle_type,
            "license_plate": self.license_plate,
            "current_status": self.current_status,
            "current_location": self.current_location,
            "location_updated_at": self.location_updated_at.isoformat() if self.location_updated_at else None
        })
        return base
