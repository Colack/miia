import bcrypt
import json

class AuthManager:
    """Manages user accounts and permissions."""

    def __init__(self, user_file="users.json"):
        self.user_file = user_file
        self.users = self.load_users()

    def load_users(self):
        """Load users from the JSON file."""
        try:
            with open(self.user_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        """Save users to the JSON file."""
        with open(self.user_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, username, password, role="staff"):
        """Add a new user (pending approval)."""
        if username in self.users:
            raise ValueError("User already exists")
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.users[username] = {
            "password": hashed_pw,
            "role": role,
            "status": "pending"
        }
        self.save_users()

    def authenticate(self, username, password):
        """Authenticate a user."""
        user = self.users.get(username)
        if not user or user["status"] != "active":
            return False
        return bcrypt.checkpw(password.encode(), user["password"].encode())

    def get_role(self, username):
        """Get the role of a user."""
        return self.users.get(username, {}).get("role", None)

    def get_pending_users(self):
        """Get all users pending approval."""
        return {user: data for user, data in self.users.items() if data["status"] == "pending"}

    def approve_user(self, username):
        """Approve a pending user."""
        if username in self.users and self.users[username]["status"] == "pending":
            self.users[username]["status"] = "active"
            self.save_users()

    def reject_user(self, username):
        """Reject (delete) a pending user."""
        if username in self.users and self.users[username]["status"] == "pending":
            del self.users[username]
            self.save_users()
