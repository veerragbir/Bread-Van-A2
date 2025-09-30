from App.models import User, Resident, Driver, UserType
from App.database import db
from enum import Enum

class UserController:
    @staticmethod
    def create_user(user_type, username, password, email, name, **kwargs):
        """Create a new user based on type - Extended for Bread Van App"""
        try:
            if user_type == UserType.RESIDENT:
                if 'home_address' not in kwargs:
                    return None, "Home address required for resident"
                user = Resident(username, password, email, name, kwargs['home_address'])
            elif user_type == UserType.DRIVER:
                if 'vehicle_type' not in kwargs or 'license_plate' not in kwargs:
                    return None, "Vehicle type and license plate required for driver"
                user = Driver(username, password, email, name, kwargs['vehicle_type'], kwargs['license_plate'])
            else:
                # Fallback to basic User for template compatibility
                user = User(username, password, email, name, user_type)
            
            db.session.add(user)
            db.session.commit()
            return user, "User created successfully"
            
        except Exception as e:
            db.session.rollback()
            return None, f"Error creating user: {str(e)}"

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return db.session.get(User, user_id)

    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all_users():
        """Get all users"""
        return User.query.all()

    @staticmethod
    def get_all_residents():
        """Get all residents - Bread Van App specific"""
        return Resident.query.all()

    @staticmethod
    def get_all_drivers():
        """Get all drivers - Bread Van App specific"""
        return Driver.query.all()

    @staticmethod
    def authenticate(username, password):
        """Authenticate user"""
        user = UserController.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None

    # Keep existing template functions for compatibility
    @staticmethod
    def create_user_basic(username, password):
        """Original template function for basic user creation"""
        user = UserController.get_user_by_username(username)
        if user:
            return None, "User already exists"
        newuser = User(username=username, password=password)
        db.session.add(newuser)
        db.session.commit()
        return newuser, "User created"

    @staticmethod
    def get_all_users_json():
        """Original template function"""
        users = UserController.get_all_users()
        if not users:
            return []
        users = [user.get_json() for user in users]
        return users

# Keep the original functions for template compatibility
def create_user(username, password):
    return UserController.create_user_basic(username, password)

def get_all_users_json():
    return UserController.get_all_users_json()

def get_all_users():
    return UserController.get_all_users()

def get_user(id):
    return UserController.get_user_by_id(id)

def get_user_by_username(username):
    return UserController.get_user_by_username(username)

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.commit()
        return user
    return None

