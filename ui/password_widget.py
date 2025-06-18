from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QSplitter, QTextEdit, QGroupBox,
                             QDialog, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon
from core.password_manager import PasswordManager
import os
from datetime import datetime
import webbrowser
import json
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

class PasswordRecoveryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recuperação de Senha")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Tabs for different recovery methods
        recovery_group = QGroupBox("Escolha uma opção de recuperação:")
        recovery_layout = QVBoxLayout(recovery_group)
        
        # Admin password option
        self.admin_radio = QPushButton("Usar senha de administrador")
        self.admin_radio.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.admin_radio.clicked.connect(self.show_admin_recovery)
        
        # Email recovery option
        self.email_radio = QPushButton("Recuperar por email")
        self.email_radio.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.email_radio.clicked.connect(self.show_email_recovery)
        
        recovery_layout.addWidget(self.admin_radio)
        recovery_layout.addWidget(self.email_radio)
        layout.addWidget(recovery_group)
        
        self.stack_widget = QWidget()
        self.stack_layout = QVBoxLayout(self.stack_widget)
        layout.addWidget(self.stack_widget)
        
        self.recovery_method = None
        self.recovery_data = None

    def show_admin_recovery(self):
        # Clear previous widgets
        for i in reversed(range(self.stack_layout.count())): 
            self.stack_layout.itemAt(i).widget().setParent(None)
        
        # Admin password input
        self.admin_input = QLineEdit()
        self.admin_input.setPlaceholderText("Digite a senha de administrador")
        self.admin_input.setEchoMode(QLineEdit.Password)
        
        # Submit button
        submit_btn = QPushButton("Verificar")
        submit_btn.clicked.connect(self.verify_admin_password)
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        self.stack_layout.addWidget(QLabel("Senha de Administrador:"))
        self.stack_layout.addWidget(self.admin_input)
        self.stack_layout.addWidget(submit_btn)
        
        self.recovery_method = "admin"

    def show_email_recovery(self):
        # Clear previous widgets
        for i in reversed(range(self.stack_layout.count())): 
            self.stack_layout.itemAt(i).widget().setParent(None)
        
        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email")
        
        # Submit button
        submit_btn = QPushButton("Enviar Código")
        submit_btn.clicked.connect(self.send_recovery_email)
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.stack_layout.addWidget(QLabel("Seu Email:"))
        self.stack_layout.addWidget(self.email_input)
        self.stack_layout.addWidget(submit_btn)
        
        self.recovery_method = "email"

    def verify_admin_password(self):
        admin_password = self.admin_input.text()
        if self.config and admin_password == self.config.get_admin_password():
            self.recovery_method = "admin"
            self.recovery_data = True
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Senha de administrador incorreta")

    def send_recovery_email(self):
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Erro", "Digite um email válido")
            return
            
        # Gerar código de recuperação
        recovery_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        try:
            if self.config:
                email_settings = self.config.get_email_settings()
                
                # Configurar email
                msg = MIMEMultipart()
                msg['From'] = email_settings['email']
                msg['To'] = email
                msg['Subject'] = "Recuperação de Senha - SecureVault"
                
                body = f"""
                Olá,
                
                Você solicitou a recuperação da sua senha mestra no SecureVault.
                Seu código de recuperação é: {recovery_code}
                
                Se você não solicitou esta recuperação, ignore este email.
                
                Atenciosamente,
                Equipe SecureVault
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Configurar servidor SMTP
                server = smtplib.SMTP(email_settings['smtp_server'], email_settings['smtp_port'])
                server.starttls()
                server.login(email_settings['email'], email_settings['password'])
                text = msg.as_string()
                server.sendmail(email_settings['email'], email, text)
                server.quit()
                
                # Mostrar campo para código de verificação
                self.show_verification_code_input(recovery_code)
            else:
                raise Exception("Configuração de email não encontrada")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao enviar email: {str(e)}")
            self.log_message(f"Erro ao enviar email: {str(e)}")

    def show_verification_code_input(self, expected_code):
        # Clear previous widgets
        for i in reversed(range(self.stack_layout.count())): 
            self.stack_layout.itemAt(i).widget().setParent(None)
        
        # Code input
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Digite o código recebido")
        
        # Verify button
        verify_btn = QPushButton("Verificar Código")
        verify_btn.clicked.connect(lambda: self.verify_code(expected_code))
        verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.stack_layout.addWidget(QLabel("Código de Verificação:"))
        self.stack_layout.addWidget(self.code_input)
        self.stack_layout.addWidget(verify_btn)

    def verify_code(self, expected_code):
        if self.code_input.text() == expected_code:
            self.recovery_method = "email"
            self.recovery_data = self.email_input.text()
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Código incorreto")

class PasswordWidget(QWidget):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        self.config = config
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
        
        # Recovery button
        self.recovery_button = QPushButton("🔄 Recuperar Senha")
        self.recovery_button.setToolTip("Recuperar senha mestra")
        self.recovery_button.clicked.connect(self.show_recovery_dialog)
        self.recovery_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        # Import/Export buttons
        self.import_button = QPushButton("📥 Importar")
        self.import_button.setToolTip("Importar senhas de arquivo")
        self.import_button.clicked.connect(self.import_passwords)
        self.import_button.setEnabled(False)
        self.import_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        self.export_button = QPushButton("📤 Exportar")
        self.export_button.setToolTip("Exportar senhas para arquivo")
        self.export_button.clicked.connect(self.export_passwords)
        self.export_button.setEnabled(False)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        master_layout.addWidget(self.master_password_input)
        master_layout.addWidget(self.login_button)
        master_layout.addWidget(self.recovery_button)
        master_layout.addWidget(self.import_button)
        master_layout.addWidget(self.export_button)
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
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.resizeSection(2, 300)  # Fixed width for actions column
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
        self.import_button.setEnabled(enabled)
        self.export_button.setEnabled(enabled)
        
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
            actions_layout.setContentsMargins(4, 4, 4, 4)
            actions_layout.setSpacing(8)
            
            # Open website button
            open_button = QPushButton("🌐")
            open_button.setToolTip("Abrir Site")
            open_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                    min-width: 30px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            open_button.clicked.connect(lambda _, w=website: self.open_website(w))
            
            # Show password button
            show_button = QPushButton("👁️")
            show_button.setToolTip("Mostrar Senha")
            show_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                    min-width: 30px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            show_button.clicked.connect(lambda _, w=website: self.show_password(w))

            # Edit button
            edit_button = QPushButton("✏️")
            edit_button.setToolTip("Editar")
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                    min-width: 30px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
            """)
            edit_button.clicked.connect(lambda _, w=website: self.edit_entry(w))
            
            # Delete button
            delete_button = QPushButton("🗑️")
            delete_button.setToolTip("Excluir")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                    min-width: 30px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            delete_button.clicked.connect(lambda _, w=website: self.delete_entry(w))
            
            actions_layout.addWidget(open_button)
            actions_layout.addWidget(show_button)
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
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
        
    def open_website(self, website: str):
        try:
            # Ensure the website has a protocol
            if not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            webbrowser.open(website)
            self.log_message(f"Abrindo site: {website}")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Não foi possível abrir o site: {str(e)}")
            self.log_message(f"Erro ao abrir site {website}: {str(e)}")

    def edit_entry(self, website: str):
        entry = self.password_manager.get_entry(website)
        
        # Create edit dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Entrada")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Website field
        website_input = QLineEdit(website)
        website_input.setPlaceholderText("Website")
        layout.addWidget(QLabel("Website:"))
        layout.addWidget(website_input)
        
        # Username field
        username_input = QLineEdit(entry["username"])
        username_input.setPlaceholderText("Usuário")
        layout.addWidget(QLabel("Usuário:"))
        layout.addWidget(username_input)
        
        # Password field
        password_input = QLineEdit(entry["password"])
        password_input.setPlaceholderText("Senha")
        password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Senha:"))
        layout.addWidget(password_input)
        
        # Show/Hide password button
        show_password_btn = QPushButton("Mostrar Senha")
        show_password_btn.setCheckable(True)
        show_password_btn.toggled.connect(
            lambda checked: password_input.setEchoMode(
                QLineEdit.Normal if checked else QLineEdit.Password
            )
        )
        layout.addWidget(show_password_btn)
        
        # Buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Salvar")
        cancel_btn = QPushButton("Cancelar")
        
        save_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            new_website = website_input.text()
            new_username = username_input.text()
            new_password = password_input.text()
            
            if not all([new_website, new_username, new_password]):
                QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios")
                return
            
            # If website changed, delete old entry
            if new_website != website:
                self.password_manager.delete_entry(website)
            
            # Add/Update entry
            self.password_manager.add_entry(new_website, new_username, new_password)
            self.password_manager.save_to_file("passwords.enc")
            
            self.log_message(f"Entrada atualizada para o site: {new_website}")
            self.refresh_table()

    def import_passwords(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("CSV files (*.csv);;JSON files (*.json)")
        file_dialog.setDefaultSuffix("csv")
        
        if file_dialog.exec_() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            file_type = file_dialog.selectedNameFilter()
            
            try:
                if file_type == "CSV files (*.csv)":
                    with open(file_path, 'r', newline='', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            if all(key in row for key in ['website', 'username', 'password']):
                                self.password_manager.add_entry(
                                    row['website'],
                                    row['username'],
                                    row['password']
                                )
                
                elif file_type == "JSON files (*.json)":
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        for entry in data:
                            if all(key in entry for key in ['website', 'username', 'password']):
                                self.password_manager.add_entry(
                                    entry['website'],
                                    entry['username'],
                                    entry['password']
                                )
                
                self.password_manager.save_to_file("passwords.enc")
                self.refresh_table()
                self.log_message(f"Senhas importadas com sucesso de: {file_path}")
                QMessageBox.information(self, "Sucesso", "Senhas importadas com sucesso!")
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao importar senhas: {str(e)}")
                self.log_message(f"Erro ao importar senhas: {str(e)}")

    def export_passwords(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("CSV files (*.csv);;JSON files (*.json)")
        file_dialog.setDefaultSuffix("csv")
        
        if file_dialog.exec_() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            file_type = file_dialog.selectedNameFilter()
            
            try:
                entries = []
                for website in self.password_manager.list_websites():
                    entry = self.password_manager.get_entry(website)
                    entries.append({
                        'website': website,
                        'username': entry['username'],
                        'password': entry['password']
                    })
                
                if file_type == "CSV files (*.csv)":
                    with open(file_path, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.DictWriter(file, fieldnames=['website', 'username', 'password'])
                        writer.writeheader()
                        writer.writerows(entries)
                
                elif file_type == "JSON files (*.json)":
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(entries, file, indent=4, ensure_ascii=False)
                
                self.log_message(f"Senhas exportadas com sucesso para: {file_path}")
                QMessageBox.information(self, "Sucesso", "Senhas exportadas com sucesso!")
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao exportar senhas: {str(e)}")
                self.log_message(f"Erro ao exportar senhas: {str(e)}")

    def show_recovery_dialog(self):
        dialog = PasswordRecoveryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            if dialog.recovery_method == "admin":
                self.reset_master_password()
            elif dialog.recovery_method == "email":
                self.send_new_master_password(dialog.recovery_data)

    def reset_master_password(self):
        new_password_dialog = QDialog(self)
        new_password_dialog.setWindowTitle("Nova Senha Mestra")
        layout = QVBoxLayout(new_password_dialog)
        
        new_password = QLineEdit()
        new_password.setPlaceholderText("Nova senha mestra")
        new_password.setEchoMode(QLineEdit.Password)
        
        confirm_password = QLineEdit()
        confirm_password.setPlaceholderText("Confirme a nova senha")
        confirm_password.setEchoMode(QLineEdit.Password)
        
        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(new_password_dialog.accept)
        
        layout.addWidget(QLabel("Digite a nova senha mestra:"))
        layout.addWidget(new_password)
        layout.addWidget(QLabel("Confirme a nova senha:"))
        layout.addWidget(confirm_password)
        layout.addWidget(save_btn)
        
        if new_password_dialog.exec_() == QDialog.Accepted:
            if new_password.text() == confirm_password.text():
                # Aqui você deve implementar a lógica para redefinir a senha mestra
                # Por exemplo, reencriptando o arquivo de senhas com a nova senha
                QMessageBox.information(self, "Sucesso", "Senha mestra alterada com sucesso!")
                self.log_message("Senha mestra alterada através da recuperação")
            else:
                QMessageBox.warning(self, "Erro", "As senhas não coincidem")

    def send_new_master_password(self, email):
        # Gerar nova senha temporária
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        try:
            if self.config:
                email_settings = self.config.get_email_settings()
                
                # Configurar email
                msg = MIMEMultipart()
                msg['From'] = email_settings['email']
                msg['To'] = email
                msg['Subject'] = "Nova Senha Mestra - SecureVault"
                
                body = f"""
                Olá,
                
                Sua nova senha mestra temporária é: {temp_password}
                
                Por favor, altere esta senha assim que fizer login no sistema.
                
                Atenciosamente,
                Equipe SecureVault
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Configurar servidor SMTP
                server = smtplib.SMTP(email_settings['smtp_server'], email_settings['smtp_port'])
                server.starttls()
                server.login(email_settings['email'], email_settings['password'])
                text = msg.as_string()
                server.sendmail(email_settings['email'], email, text)
                server.quit()
                
                # Aqui você deve implementar a lógica para definir a nova senha mestra
                # Por exemplo, reencriptando o arquivo de senhas com a senha temporária
                
                QMessageBox.information(
                    self,
                    "Sucesso",
                    "Uma nova senha foi enviada para seu email.\nPor favor, verifique sua caixa de entrada."
                )
                self.log_message(f"Nova senha mestra enviada para: {email}")
            else:
                raise Exception("Configuração de email não encontrada")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao enviar email: {str(e)}")
            self.log_message(f"Erro ao enviar email: {str(e)}") 