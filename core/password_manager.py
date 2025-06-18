from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
import os
from typing import Dict, List, Optional

class PasswordManager:
    def __init__(self, master_password: str):
        self.salt = os.urandom(16)
        self.key = self._generate_key(master_password)
        self.cipher_suite = Fernet(self.key)
        self.passwords: Dict[str, Dict[str, str]] = {}
        
    def _generate_key(self, password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def add_entry(self, website: str, username: str, password: str) -> None:
        """Add a new password entry."""
        encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()
        self.passwords[website] = {
            "username": username,
            "password": encrypted_password
        }
    
    def get_entry(self, website: str) -> Optional[Dict[str, str]]:
        """Get a password entry."""
        if website not in self.passwords:
            return None
            
        entry = self.passwords[website].copy()
        entry["password"] = self.cipher_suite.decrypt(
            entry["password"].encode()
        ).decode()
        return entry
    
    def list_websites(self) -> List[str]:
        """List all stored websites."""
        return list(self.passwords.keys())
    
    def delete_entry(self, website: str) -> bool:
        """Delete a password entry."""
        if website in self.passwords:
            del self.passwords[website]
            return True
        return False
    
    def save_to_file(self, filename: str) -> None:
        """Save passwords to encrypted file."""
        data = {
            "salt": base64.b64encode(self.salt).decode(),
            "passwords": self.passwords
        }
        encrypted_data = self.cipher_suite.encrypt(json.dumps(data).encode())
        with open(filename, "wb") as f:
            f.write(encrypted_data)
    
    @classmethod
    def load_from_file(cls, filename: str, master_password: str) -> "PasswordManager":
        """Load passwords from encrypted file."""
        with open(filename, "rb") as f:
            encrypted_data = f.read()
            
        # Create temporary instance to decrypt
        temp_manager = cls(master_password)
        
        try:
            decrypted_data = json.loads(temp_manager.cipher_suite.decrypt(encrypted_data))
            temp_manager.salt = base64.b64decode(decrypted_data["salt"])
            temp_manager.key = temp_manager._generate_key(master_password)
            temp_manager.cipher_suite = Fernet(temp_manager.key)
            temp_manager.passwords = decrypted_data["passwords"]
            return temp_manager
        except Exception as e:
            raise ValueError("Invalid master password or corrupted file") from e 