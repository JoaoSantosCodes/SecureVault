from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QTextEdit, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from core.password_manager import PasswordManager
import os
from datetime import datetime

class PasswordWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.password_manager = None
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Criar um splitter vertical para dividir a interface
        splitter = QSplitter(Qt.Vertical)
        
        # Widget superior para conteúdo existente
        top_widget = QWidget()
        layout = QVBoxLayout(top_widget)
        
        # Master password section
        master_layout = QHBoxLayout()
        self.master_password_input = QLineEdit()
        self.master_password_input.setPlaceholderText("Digite a senha mestra")
        self.master_password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.login)
        master_layout.addWidget(self.master_password_input)
        master_layout.addWidget(self.login_button)
        layout.addLayout(master_layout)
        
        # Add new entry section
        entry_layout = QHBoxLayout()
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Website")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.add_button = QPushButton("Adicionar")
        self.add_button.clicked.connect(self.add_entry)
        
        entry_layout.addWidget(self.website_input)
        entry_layout.addWidget(self.username_input)
        entry_layout.addWidget(self.password_input)
        entry_layout.addWidget(self.add_button)
        layout.addLayout(entry_layout)
        
        # Password table
        self.password_table = QTableWidget(0, 3)
        self.password_table.setHorizontalHeaderLabels(["Website", "Usuário", "Ações"])
        header = self.password_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        layout.addWidget(self.password_table)
        
        # Adicionar widget superior ao splitter
        splitter.addWidget(top_widget)
        
        # Criar e configurar o painel de log
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setStyleSheet("""
            QTextEdit {
                background-color: #232323;
                color: #44ff44;
                border: 1px solid #44ff44;
                border-radius: 4px;
                font-family: Consolas, monospace;
                font-size: 10pt;
            }
        """)
        self.log_panel.setMinimumHeight(150)
        self.log_panel.setMaximumHeight(200)
        
        # Adicionar painel de log ao splitter
        splitter.addWidget(self.log_panel)
        
        # Adicionar splitter ao layout principal
        main_layout.addWidget(splitter)
        
        # Disable inputs initially
        self.set_inputs_enabled(False)
        
        # Log inicial
        self.log_message("Sistema iniciado. Aguardando login...")
        
    def log_message(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_panel.append(f"[{timestamp}] {message}")
        
    def set_inputs_enabled(self, enabled: bool):
        self.website_input.setEnabled(enabled)
        self.username_input.setEnabled(enabled)
        self.password_input.setEnabled(enabled)
        self.add_button.setEnabled(enabled)
        self.password_table.setEnabled(enabled)
        
    def login(self):
        master_password = self.master_password_input.text()
        if not master_password:
            QMessageBox.warning(self, "Erro", "Digite a senha mestra")
            self.log_message("Tentativa de login sem senha mestra")
            return
            
        try:
            if os.path.exists("passwords.enc"):
                self.password_manager = PasswordManager.load_from_file(
                    "passwords.enc", master_password
                )
                self.log_message("Arquivo de senhas carregado com sucesso")
            else:
                self.password_manager = PasswordManager(master_password)
                self.log_message("Novo gerenciador de senhas criado")
            
            self.set_inputs_enabled(True)
            self.master_password_input.setEnabled(False)
            self.login_button.setEnabled(False)
            self.refresh_table()
            self.log_message("Login realizado com sucesso")
            
        except ValueError:
            QMessageBox.critical(self, "Erro", "Senha mestra inválida")
            self.log_message("Falha no login: senha mestra inválida")
            
    def add_entry(self):
        website = self.website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not all([website, username, password]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos")
            self.log_message("Tentativa de adicionar entrada com campos vazios")
            return
            
        self.password_manager.add_entry(website, username, password)
        self.password_manager.save_to_file("passwords.enc")
        
        self.log_message(f"Nova entrada adicionada para o site: {website}")
        
        self.website_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        
        self.refresh_table()
        
    def refresh_table(self):
        self.password_table.setRowCount(0)
        for website in self.password_manager.list_websites():
            entry = self.password_manager.get_entry(website)
            row = self.password_table.rowCount()
            self.password_table.insertRow(row)
            
            self.password_table.setItem(row, 0, QTableWidgetItem(website))
            self.password_table.setItem(row, 1, QTableWidgetItem(entry["username"]))
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            show_button = QPushButton("Mostrar")
            show_button.clicked.connect(lambda _, w=website: self.show_password(w))
            delete_button = QPushButton("Excluir")
            delete_button.clicked.connect(lambda _, w=website: self.delete_entry(w))
            
            actions_layout.addWidget(show_button)
            actions_layout.addWidget(delete_button)
            self.password_table.setCellWidget(row, 2, actions_widget)
            
    def show_password(self, website: str):
        entry = self.password_manager.get_entry(website)
        QMessageBox.information(
            self,
            "Senha",
            f"Website: {website}\nUsuário: {entry['username']}\nSenha: {entry['password']}"
        )
        self.log_message(f"Senha visualizada para o site: {website}")
        
    def delete_entry(self, website: str):
        reply = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir a entrada para {website}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.password_manager.delete_entry(website)
            self.password_manager.save_to_file("passwords.enc")
            self.refresh_table()
            self.log_message(f"Entrada excluída para o site: {website}") 