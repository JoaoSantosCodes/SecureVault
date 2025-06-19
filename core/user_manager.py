import json
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import uuid

class UserManager:
    def __init__(self):
        # Criar diretório de dados se não existir
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.users_file = os.path.join(self.data_dir, "users.enc")
        self.key_file = os.path.join(self.data_dir, "users.key")
        self._load_or_create_key()
        self._load_or_create_users()
        
    def _generate_key(self):
        return Fernet.generate_key()
    
    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = self._generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
        self.fernet = Fernet(self.key)
    
    def _load_or_create_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                self.users = json.loads(decrypted_data)
        else:
            self.users = {
                "profiles": {},
                "email_map": {}  # Mapeia emails para IDs de usuário
            }
            self.save_users()
    
    def save_users(self):
        encrypted_data = self.fernet.encrypt(json.dumps(self.users).encode())
        with open(self.users_file, 'wb') as f:
            f.write(encrypted_data)
    
    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.b64encode(kdf.derive(password.encode()))
        return salt, key.decode('utf-8')
    
    def create_user(self, username, password, email, is_admin=False):
        if username in self.users["profiles"]:
            raise ValueError("Usuário já existe")
        
        if email in self.users["email_map"]:
            raise ValueError("Email já está em uso")
        
        user_id = str(uuid.uuid4())
        salt, hashed_password = self._hash_password(password)
        
        # Criar diretório para os arquivos do usuário
        user_dir = os.path.join(self.data_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        self.users["profiles"][username] = {
            "id": user_id,
            "salt": base64.b64encode(salt).decode('utf-8'),
            "password": hashed_password,
            "email": email,
            "is_admin": is_admin,
            "settings": {
                "theme": "dark",
                "auto_logout": 30,  # minutos
                "password_file": os.path.join(user_dir, "passwords.enc")
            }
        }
        
        self.users["email_map"][email] = user_id
        self.save_users()
        return user_id
    
    def verify_password(self, username, password):
        if username not in self.users["profiles"]:
            return False
        
        user = self.users["profiles"][username]
        salt = base64.b64decode(user["salt"])
        _, hashed_password = self._hash_password(password, salt)
        
        return hashed_password == user["password"]
    
    def get_user_by_email(self, email):
        if email in self.users["email_map"]:
            user_id = self.users["email_map"][email]
            for username, user in self.users["profiles"].items():
                if user["id"] == user_id:
                    return username, user
        return None, None
    
    def get_user_settings(self, username):
        if username in self.users["profiles"]:
            return self.users["profiles"][username]["settings"]
        return None
    
    def update_user_settings(self, username, settings):
        if username in self.users["profiles"]:
            self.users["profiles"][username]["settings"].update(settings)
            self.save_users()
            return True
        return False
    
    def change_password(self, username, new_password):
        if username in self.users["profiles"]:
            salt, hashed_password = self._hash_password(new_password)
            self.users["profiles"][username]["salt"] = base64.b64encode(salt).decode('utf-8')
            self.users["profiles"][username]["password"] = hashed_password
            self.save_users()
            return True
        return False
    
    def is_admin(self, username):
        if username in self.users["profiles"]:
            return self.users["profiles"][username]["is_admin"]
        return False
    
    def get_user_id(self, username):
        if username in self.users["profiles"]:
            return self.users["profiles"][username]["id"]
        return None 