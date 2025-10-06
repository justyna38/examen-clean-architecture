from enum import Enum
from typing import Optional

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class User:
    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role

class AuthService:
    def __init__(self):
        self.users = {
            "admin": User("admin", Role.ADMIN),
            "user": User("user", Role.USER)
        }
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        # Note: In production, use proper password hashing (bcrypt, scrypt, etc.)
        # This is just for demonstration purposes
        if username in self.users and password == "password":  # nosec B105
            return self.users[username]
        return None
    
    def has_permission(self, user: User, action: str) -> bool:
        if user.role == Role.ADMIN:
            return True
        if user.role == Role.USER and action in ["read", "upload"]:
            return True
        return False