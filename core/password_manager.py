from cryptography.fernet import Fernet
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class PasswordManager:
    def __init__(self, password_file: str):
        self.password_file = password_file
        self.key_file = f"{password_file}.key"
        self._load_or_create()
    
    def _generate_key(self):
        return Fernet.generate_key()
    
    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            # Criar o diretório se não existir
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            key = self._generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _load_or_create(self):
        key = self._load_or_create_key()
        self.fernet = Fernet(key)
        
        if os.path.exists(self.password_file):
            with open(self.password_file, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                data = json.loads(decrypted_data)
                # Migrar formato antigo se necessário
                if isinstance(data, dict) and not ("groups" in data and "default_group" in data):
                    self.passwords = {
                        "groups": {
                            "Geral": data  # Mover senhas existentes para o grupo Geral
                        },
                        "default_group": "Geral"
                    }
                    self.save()
                else:
                    self.passwords = data
        else:
            # Criar o diretório se não existir
            os.makedirs(os.path.dirname(self.password_file), exist_ok=True)
            self.passwords = {
                "groups": {
                    "Geral": {}  # Grupo padrão
                },
                "default_group": "Geral"
            }
            self.save()
    
    def save(self):
        encrypted_data = self.fernet.encrypt(json.dumps(self.passwords).encode())
        with open(self.password_file, 'wb') as f:
            f.write(encrypted_data)
    
    def create_group(self, group_name: str) -> None:
        """Create a new password group."""
        if group_name in self.passwords["groups"]:
            raise ValueError(f"Grupo {group_name} já existe")
        
        self.passwords["groups"][group_name] = {}
        self.save()
    
    def delete_group(self, group_name: str) -> bool:
        """Delete a password group."""
        if group_name == "Geral":
            raise ValueError("Não é possível excluir o grupo Geral")
        
        if group_name in self.passwords["groups"]:
            del self.passwords["groups"][group_name]
            self.save()
            return True
        return False
    
    def list_groups(self) -> List[str]:
        """List all password groups."""
        return list(self.passwords["groups"].keys())
    
    def add_entry(self, website: str, username: str, password: str, group: str = None) -> None:
        """Add a new password entry."""
        if group is None:
            group = self.passwords["default_group"]
        
        if group not in self.passwords["groups"]:
            raise ValueError(f"Grupo {group} não existe")
        
        if website in self.passwords["groups"][group]:
            raise ValueError(f"Entrada para {website} já existe no grupo {group}")
            
        self.passwords["groups"][group][website] = {
            "username": username,
            "password": self.fernet.encrypt(password.encode()).decode(),
            "last_modified": datetime.now().timestamp()
        }
        self.save()
    
    def get_entry(self, website: str, group: str = None) -> Optional[Dict[str, str]]:
        """Get a password entry."""
        if group is None:
            # Procurar em todos os grupos
            for group_name, entries in self.passwords["groups"].items():
                if website in entries:
                    entry = entries[website].copy()
                    entry["password"] = self.fernet.decrypt(
                        entry["password"].encode()
                    ).decode()
                    entry["group"] = group_name
                    return entry
            return None
        
        if group not in self.passwords["groups"]:
            raise ValueError(f"Grupo {group} não existe")
            
        if website not in self.passwords["groups"][group]:
            return None
            
        entry = self.passwords["groups"][group][website].copy()
        entry["password"] = self.fernet.decrypt(
            entry["password"].encode()
        ).decode()
        entry["group"] = group
        return entry
    
    def get_password(self, website: str, group: str = None) -> str:
        """Get password for a website."""
        entry = self.get_entry(website, group)
        if entry is None:
            raise ValueError(f"Entrada para {website} não encontrada")
        return entry["password"]
    
    def get_all_entries(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Get all password entries organized by groups."""
        return self.passwords["groups"]
    
    def update_entry(self, website: str, username: str, password: str, group: str = None) -> None:
        """Update an existing password entry."""
        if group is None:
            # Procurar em todos os grupos
            for group_name, entries in self.passwords["groups"].items():
                if website in entries:
                    group = group_name
                    break
            if group is None:
                raise ValueError(f"Entrada para {website} não encontrada")
        
        if group not in self.passwords["groups"]:
            raise ValueError(f"Grupo {group} não existe")
            
        if website not in self.passwords["groups"][group]:
            raise ValueError(f"Entrada para {website} não encontrada no grupo {group}")
            
        self.passwords["groups"][group][website] = {
            "username": username,
            "password": self.fernet.encrypt(password.encode()).decode(),
            "last_modified": datetime.now().timestamp()
        }
        self.save()
    
    def delete_entry(self, website: str, group: str = None) -> bool:
        """Delete a password entry."""
        if group is None:
            # Procurar em todos os grupos
            for group_name, entries in self.passwords["groups"].items():
                if website in entries:
                    del self.passwords["groups"][group_name][website]
                    self.save()
                    return True
            return False
        
        if group not in self.passwords["groups"]:
            return False
            
        if website in self.passwords["groups"][group]:
            del self.passwords["groups"][group][website]
            self.save()
            return True
        return False
    
    def move_entry(self, website: str, from_group: str, to_group: str) -> bool:
        """Move a password entry from one group to another."""
        if from_group not in self.passwords["groups"] or to_group not in self.passwords["groups"]:
            return False
            
        if website not in self.passwords["groups"][from_group]:
            return False
            
        entry = self.passwords["groups"][from_group][website]
        self.passwords["groups"][to_group][website] = entry
        del self.passwords["groups"][from_group][website]
        self.save()
        return True
    
    def set_default_group(self, group: str) -> bool:
        """Set the default group for new entries."""
        if group not in self.passwords["groups"]:
            return False
        self.passwords["default_group"] = group
        self.save()
        return True
    
    def get_default_group(self) -> str:
        """Get the default group name."""
        return self.passwords["default_group"] 