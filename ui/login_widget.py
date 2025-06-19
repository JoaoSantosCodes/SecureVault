from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QDialog)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import os

class LoginWidget(QDialog):
    loginSuccessful = pyqtSignal(str)  # Emite o nome de usuário após login bem-sucedido
    registerRequested = pyqtSignal()
    
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("SecureVault - Login")
        self.setFixedSize(400, 200)
        
        # Definir ícone da janela
        icon_path = os.path.join("resources", "images", "SecureVault-Icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        layout = QVBoxLayout()
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Usuário:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Botões
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Entrar")
        self.register_button = QPushButton("Registrar")
        self.forgot_password_button = QPushButton("Esqueci a Senha")
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.forgot_password_button)
        
        # Conectar sinais
        self.login_button.clicked.connect(self.try_login)
        self.register_button.clicked.connect(self.registerRequested.emit)
        self.forgot_password_button.clicked.connect(self.forgot_password)
        
        # Adicionar layouts ao layout principal
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return
        
        if self.user_manager.verify_password(username, password):
            self.loginSuccessful.emit(username)
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.")
            self.password_input.clear()
    
    def forgot_password(self):
        username = self.username_input.text()
        if not username:
            QMessageBox.warning(self, "Erro", "Digite seu nome de usuário para recuperar a senha.")
            return
            
        user_data = self.user_manager.get_user_by_email(username)
        if user_data:
            # Implementar lógica de recuperação de senha
            QMessageBox.information(self, "Recuperação de Senha", 
                                 "Um email de recuperação será enviado para o endereço cadastrado.")
        else:
            QMessageBox.warning(self, "Erro", "Usuário não encontrado.")

class RegisterWidget(QDialog):
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("SecureVault - Registro")
        self.setFixedSize(400, 250)
        
        # Definir ícone da janela
        icon_path = os.path.join("resources", "images", "SecureVault-Icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        layout = QVBoxLayout()
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Usuário:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Confirm Password
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirmar Senha:")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        
        # Botões
        button_layout = QHBoxLayout()
        self.register_button = QPushButton("Registrar")
        self.cancel_button = QPushButton("Cancelar")
        
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.cancel_button)
        
        # Conectar sinais
        self.register_button.clicked.connect(self.try_register)
        self.cancel_button.clicked.connect(self.reject)
        
        # Adicionar layouts ao layout principal
        layout.addLayout(username_layout)
        layout.addLayout(email_layout)
        layout.addLayout(password_layout)
        layout.addLayout(confirm_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def try_register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not all([username, email, password, confirm]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem.")
            self.password_input.clear()
            self.confirm_input.clear()
            return
        
        try:
            self.user_manager.create_user(username, password, email)
            QMessageBox.information(self, "Sucesso", "Usuário registrado com sucesso!")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e)) 