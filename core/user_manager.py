import os
import json
import bcrypt
import logging

class UserManager:
    def __init__(self, user_file="data/users.json"):
        self.user_file = user_file
        self.load_users()
        
    def load_users(self):
        if os.path.exists(self.user_file):
            with open(self.user_file, "r") as file:
                self.users = json.load(file)
        else:
            self.users = {}
            
    def save_users(self):
        with open(self.user_file, "w") as file:
            json.dump(self.users, file, indent=4)
            
    def register_user(self, username, password):
        if username in self.users:
            logging.warning(f"User {username} already exists")
            return False
        
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.users[username] = {
            "password": hashed_password,
            "role": "user"
        }
        self.save_users()
        
    def login_user(self, username, password):
        if username not in self.users:
            logging.warning(f"User {username} does not exist")
            return False
        
        hashed_password = self.users[username]["password"]
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            return True
        else:
            return False
        
    def change_password(self, username, old_password, new_password):
        if username not in self.users:
            logging.warning(f"User {username} does not exist")
            return False
        
        hashed_password = self.users[username]["password"]
        if bcrypt.checkpw(old_password.encode(), hashed_password.encode()):
            new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            self.users[username]["password"] = new_hashed_password
            self.save_users()
            return True
        else:
            return False
        
    # NOTE: This function is only for Administrators, please don't use it for regular users
    def change_role(self, username, role):
        if username not in self.users:
            logging.warning(f"User {username} does not exist")
            return False
        
        self.users[username]["role"] = role
        self.save_users()
        return True
    
    def delete_user(self, username):
        if username not in self.users:
            logging.warning(f"User {username} does not exist")
            return False
        
        del self.users[username]
        self.save_users()
        return True
    
    def get_users(self):
        return self.users
    
    def get_user(self, username):
        if username in self.users:
            return self.users[username]
        else:
            return None
        
    def get_roles(self):
        return ["user", "admin"]
    
    def is_admin(self, username):
        if username in self.users:
            return self.users[username]["role"] == "admin"
        else:
            return False
        
    def is_user(self, username):
        if username in self.users:
            return self.users[username]["role"] == "user"
        else:
            return False
        
    def is_valid_role(self, role):
        return role in self.get_roles()
    
    def is_valid_user(self, username):
        return username in self.users