import json
import os
from cryptography.fernet import Fernet

class Config:
    def __init__(self):
        self.config_file = "config.enc"
        self.key_file = "config.key"
        self._load_or_create_config()
    
    def _generate_key(self):
        return Fernet.generate_key()
    
    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = self._generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _load_or_create_config(self):
        key = self._load_or_create_key()
        self.fernet = Fernet(key)
        
        default_config = {
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'email': 'seu_email@gmail.com',
                'password': 'sua_senha_de_app'
            },
            'app': {
                'theme': 'dark',
                'auto_logout': 30,  # minutos
                'backup_enabled': True,
                'backup_interval': 24  # horas
            }
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                self.config = json.loads(decrypted_data)
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        encrypted_data = self.fernet.encrypt(json.dumps(self.config).encode())
        with open(self.config_file, 'wb') as f:
            f.write(encrypted_data)
    
    def get_email_settings(self):
        return self.config.get('email', {})
    
    def set_email_settings(self, settings):
        self.config['email'] = settings
        self.save_config()
    
    def get_app_settings(self):
        return self.config.get('app', {})
    
    def set_app_settings(self, settings):
        self.config['app'] = settings
        self.save_config()
    
    def update_app_setting(self, key, value):
        if 'app' not in self.config:
            self.config['app'] = {}
        self.config['app'][key] = value
        self.save_config() 