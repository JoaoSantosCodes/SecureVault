from datetime import datetime
import csv
import json
import webbrowser
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                           QHeaderView, QMessageBox, QSplitter, QTextEdit, QGroupBox,
                           QDialog, QFileDialog, QListWidget, QListWidgetItem, QInputDialog,
                           QApplication, QGraphicsDropShadowEffect, QFrame)
from PyQt5.QtCore import Qt, QTimer, QSize, QPropertyAnimation
from PyQt5.QtGui import QFont, QColor, QIcon, QTextCursor
from core.password_manager import PasswordManager
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

class CustomButton(QPushButton):
    def __init__(self, text, parent=None, is_action_button=False):
        super().__init__(text, parent)
        if is_action_button:
            self.setFixedSize(32, 32)  # Aumentado para 32x32
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2b2b2b;
                    border: 1px solid #404040;
                    color: #2ecc71;
                    padding: 2px;
                    border-radius: 4px;
                    font-size: 15px;  # Fonte um pouco maior
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #353535;
                    border: 1px solid #2ecc71;
                    color: #2ecc71;
                }
                QPushButton:pressed {
                    background-color: #2ecc71;
                    border: 1px solid #2ecc71;
                    color: #1b1b1b;
                }
            """)
        else:
            self.setFixedSize(36, 36)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2b2b2b;
                    border: 2px solid #404040;
                    color: #2ecc71;
                    padding: 5px;
                    border-radius: 18px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #353535;
                    border: 2px solid #2ecc71;
                }
                QPushButton:pressed {
                    background-color: #2ecc71;
                    border: 2px solid #2ecc71;
                    color: #2b2b2b;
                }
            """)

class TypewriterTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1b1b1b;
                border: 1px solid #404040;
                color: #2ecc71;
                font-family: 'Consolas', 'Courier New', monospace;
                padding: 10px;
            }
        """)
        self.pending_text = ""
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.type_next_character)
        self.typing_timer.setInterval(50)  # 50ms entre cada caractere
        
    def append_with_animation(self, text):
        if self.typing_timer.isActive():
            # Se já está digitando, apenas adiciona ao texto pendente
            self.pending_text += "\n" + text
        else:
            self.pending_text = text
            self.typing_timer.start()
    
    def type_next_character(self):
        if not self.pending_text:
            self.typing_timer.stop()
            return
            
        # Pega o próximo caractere
        char = self.pending_text[0]
        self.pending_text = self.pending_text[1:]
        
        # Adiciona o caractere ao texto
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(char)
        self.setTextCursor(cursor)
        
        # Rola para o final
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

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
    def __init__(self, password_file, parent=None):
        super().__init__(parent)
        self.password_manager = PasswordManager(password_file)
        self.current_group = self.password_manager.get_default_group()
        self.groups_visible = False
        self.setup_ui()
        
    def setup_ui(self):
        # Definir tamanho fixo para o widget
        self.setMinimumSize(1024, 768)  # Tamanho mínimo
        self.setMaximumSize(1280, 900)  # Tamanho máximo
        
        # Definir estilo global
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTableWidget {
                gridline-color: #404040;
                border: 1px solid #404040;
                background-color: #1b1b1b;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #404040;
            }
            QTableWidget::item:selected {
                background-color: #2ecc71;
                color: #1b1b1b;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #2ecc71;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #2ecc71;
                font-weight: bold;
            }
            QListWidget {
                border: 1px solid #404040;
                background-color: #1b1b1b;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #404040;
            }
            QListWidget::item:selected {
                background-color: #2ecc71;
                color: #1b1b1b;
            }
            QLabel {
                color: #2ecc71;
                font-weight: bold;
            }
        """)
        
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)
        
        # Widget esquerdo (grupos)
        self.left_widget = QWidget()
        left_layout = QVBoxLayout(self.left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)
        
        # Label para grupos
        groups_header = QHBoxLayout()
        groups_label = QLabel("GRUPOS")
        groups_label.setStyleSheet("""
            QLabel {
                color: #2ecc71;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        groups_header.addWidget(groups_label)
        
        # Botões de grupo
        add_group_button = CustomButton("📁")
        add_group_button.setToolTip("Criar Novo Grupo")
        add_group_button.clicked.connect(self.add_group)
        groups_header.addWidget(add_group_button)
        
        delete_group_button = CustomButton("🗑️")
        delete_group_button.setToolTip("Excluir Grupo Atual")
        delete_group_button.clicked.connect(self.delete_group)
        groups_header.addWidget(delete_group_button)
        
        left_layout.addLayout(groups_header)
        
        # Lista de grupos
        self.groups_list = QListWidget()
        self.groups_list.itemClicked.connect(self.group_selected)
        left_layout.addWidget(self.groups_list)
        
        # Widget direito (principal)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        
        # Barra de ferramentas superior
        toolbar = QHBoxLayout()
        toolbar.setSpacing(5)
        
        # Botão para mostrar/ocultar grupos
        self.toggle_groups_button = CustomButton("📂")
        self.toggle_groups_button.setToolTip("Mostrar/Ocultar Painel de Grupos")
        self.toggle_groups_button.clicked.connect(self.toggle_groups)
        toolbar.addWidget(self.toggle_groups_button)
        
        # Botão de adicionar
        add_button = CustomButton("🔑")
        add_button.setToolTip("Adicionar Nova Senha")
        add_button.clicked.connect(self.add_entry)
        toolbar.addWidget(add_button)
        
        # Botão de importar
        import_button = CustomButton("📥")
        import_button.setToolTip("Importar Senhas de Arquivo (CSV/JSON)")
        import_button.clicked.connect(self.import_passwords)
        toolbar.addWidget(import_button)
        
        # Botão de exportar
        export_button = CustomButton("📤")
        export_button.setToolTip("Exportar Senhas para Arquivo (CSV/JSON)")
        export_button.clicked.connect(self.export_passwords)
        toolbar.addWidget(export_button)
        
        toolbar.addStretch()
        right_layout.addLayout(toolbar)
        
        # Tabela de senhas
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Website", "Usuário", "Senha", "Modificado", "Ações"])
        
        # Ajustar larguras das colunas e comportamento
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)  # Website - usuário pode ajustar
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)  # Usuário - usuário pode ajustar
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)    # Senha
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)    # Modificado
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)    # Ações
        
        # Larguras iniciais
        self.table.setColumnWidth(0, 200)  # Website
        self.table.setColumnWidth(1, 200)  # Usuário
        self.table.setColumnWidth(2, 120)  # Senha
        self.table.setColumnWidth(3, 100)  # Modificado
        self.table.setColumnWidth(4, 380)  # Ações (aumentado para acomodar labels)
        
        # Ajustar altura das linhas e fonte
        self.table.verticalHeader().setDefaultSectionSize(48)  # Aumentado para melhor espaçamento
        self.table.setFont(QFont("Segoe UI", 10))
        
        # Remover o cabeçalho vertical
        self.table.verticalHeader().setVisible(False)
        
        # Estilo da tabela e cabeçalhos com melhor feedback visual
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1b1b1b;
                border: 1px solid #404040;
                gridline-color: #404040;
                color: #ffffff;
                selection-background-color: #2ecc7133;
                selection-color: #ffffff;
            }
            QTableWidget::item {
                border-bottom: 1px solid #404040;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #2ecc7133;
                color: #ffffff;
                border-bottom: 1px solid #2ecc71;
            }
            QTableWidget::item:hover {
                background-color: #2b2b2b;
            }
            /* Estilo especial para células copiáveis */
            QTableWidget::item[copyable="true"]:hover {
                background-color: #2ecc7122;
                border: 1px solid #2ecc7144;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #2ecc71;
                padding: 10px;
                border: none;
                border-right: 1px solid #404040;
                border-bottom: 2px solid #2ecc71;
                font-weight: bold;
                font-size: 11px;
            }
            QTableCornerButton::section {
                background-color: #2b2b2b;
                border: none;
                border-bottom: 2px solid #2ecc71;
            }
            QScrollBar:vertical {
                background-color: #1b1b1b;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #404040;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #2ecc71;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #1b1b1b;
            }
        """)

        # Efeito de sombra mais suave
        shadow = QGraphicsDropShadowEffect(self.table)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 3)
        self.table.setGraphicsEffect(shadow)
        right_layout.addWidget(self.table)
        
        # Log de atividades com melhor visibilidade
        self.log = TypewriterTextEdit()
        self.log.setMaximumHeight(120)
        self.log.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                border: 1px solid #404040;
                border-radius: 4px;
                color: #2ecc71;
                padding: 8px;
                font-family: 'Segoe UI';
                font-size: 10pt;
            }
        """)
        right_layout.addWidget(self.log)
        
        # Adicionar widgets ao layout principal
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(right_widget)
        
        # Configurar estado inicial dos grupos
        self.left_widget.setFixedWidth(250)
        self.left_widget.hide()
        
        # Carregar dados
        self.refresh_groups()
        self.refresh_table()

    def create_action_button(self, icon, tooltip, callback):
        """Criar botão de ação com estilo personalizado."""
        button = CustomButton(icon)
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        button.setMaximumWidth(30)
        return button
    
    def toggle_groups(self):
        """Mostrar/ocultar o painel de grupos."""
        if self.left_widget.isVisible():
            self.left_widget.hide()
            self.toggle_groups_button.setText("📂")  # Pasta fechada
            self.toggle_groups_button.setStyleSheet("")
        else:
            self.left_widget.show()
            self.toggle_groups_button.setText("📂")  # Pasta aberta
            self.toggle_groups_button.setStyleSheet("background-color: #2ecc71;")
        self.log_message("Painel de grupos " + ("ocultado" if self.left_widget.isHidden() else "exibido"))
    
    def refresh_groups(self):
        """Atualizar lista de grupos."""
        self.groups_list.clear()
        for group in self.password_manager.list_groups():
            item = QListWidgetItem(group)
            if group == self.current_group:
                item.setSelected(True)
            self.groups_list.addItem(item)
    
    def group_selected(self, item):
        """Chamado quando um grupo é selecionado."""
        self.current_group = item.text()
        self.refresh_table()
        self.log_message(f"Grupo selecionado: {self.current_group}")
    
    def add_group(self):
        """Adicionar novo grupo."""
        name, ok = QInputDialog.getText(self, "Novo Grupo", "Nome do grupo:")
        if ok and name:
            try:
                self.password_manager.create_group(name)
                self.refresh_groups()
                self.log_message(f"Grupo criado: {name}")
            except ValueError as e:
                QMessageBox.warning(self, "Erro", str(e))
    
    def delete_group(self):
        """Excluir grupo selecionado."""
        if self.current_group == "Geral":
            QMessageBox.warning(self, "Erro", "Não é possível excluir o grupo Geral")
            return
        
        reply = QMessageBox.question(self, "Confirmar Exclusão",
                                   f"Tem certeza que deseja excluir o grupo {self.current_group}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.password_manager.delete_group(self.current_group)
                self.current_group = "Geral"
                self.refresh_groups()
                self.refresh_table()
                self.log_message(f"Grupo excluído: {self.current_group}")
            except ValueError as e:
                QMessageBox.warning(self, "Erro", str(e))
    
    def log_message(self, message: str):
        """Sobrescreve o método de log para usar a animação."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"  # Adicionado \n para forçar nova linha
        self.log.append_with_animation(formatted_message)
    
    def add_entry(self):
        dialog = AddEntryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            website = dialog.website_input.text()
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            
            try:
                self.password_manager.add_entry(website, username, password, self.current_group)
                self.refresh_table()
                self.log_message(f"Nova entrada adicionada para {website} no grupo {self.current_group}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))
                self.log_message(f"Erro ao adicionar entrada: {str(e)}")
    
    def show_password(self, website: str):
        try:
            password = self.password_manager.get_password(website, self.current_group)
            QMessageBox.information(self, "Senha", f"Senha para {website}: {password}")
            self.log_message(f"Senha visualizada para {website}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            self.log_message(f"Erro ao mostrar senha: {str(e)}")
    
    def delete_entry(self, website: str):
        reply = QMessageBox.question(self, "Confirmar Exclusão",
                                   f"Tem certeza que deseja excluir a entrada para {website}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.password_manager.delete_entry(website, self.current_group)
                self.refresh_table()
                self.log_message(f"Entrada deletada para {website}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))
                self.log_message(f"Erro ao deletar entrada: {str(e)}")
    
    def move_entry(self, website: str):
        groups = self.password_manager.list_groups()
        groups.remove(self.current_group)
        
        group, ok = QInputDialog.getItem(self, "Mover Entrada",
                                       "Selecione o grupo de destino:",
                                       groups, 0, False)
        
        if ok and group:
            try:
                self.password_manager.move_entry(website, self.current_group, group)
                self.refresh_table()
                self.log_message(f"Entrada {website} movida para o grupo {group}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))
                self.log_message(f"Erro ao mover entrada: {str(e)}")
    
    def open_website(self, website: str):
        try:
            if not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            webbrowser.open(website)
            self.log_message(f"Website aberto: {website}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível abrir o website: {str(e)}")
            self.log_message(f"Erro ao abrir website: {str(e)}")
    
    def edit_entry(self, website: str):
        try:
            current_data = self.password_manager.get_entry(website, self.current_group)
            dialog = EditEntryDialog(website, current_data["username"], current_data["password"], self)
            
            if dialog.exec_() == QDialog.Accepted:
                new_website = dialog.website_input.text()
                new_username = dialog.username_input.text()
                new_password = dialog.password_input.text()
                
                if website != new_website:
                    # Se o website mudou, deletar a entrada antiga e criar uma nova
                    self.password_manager.delete_entry(website, self.current_group)
                    self.password_manager.add_entry(new_website, new_username, new_password, self.current_group)
                else:
                    # Se só os dados mudaram, atualizar a entrada existente
                    self.password_manager.update_entry(website, new_username, new_password, self.current_group)
                
                self.refresh_table()
                self.log_message(f"Entrada editada para {website}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            self.log_message(f"Erro ao editar entrada: {str(e)}")
    
    def import_passwords(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Importar Senhas",
            "",
            "CSV Files (*.csv);;JSON Files (*.json)"
        )
        
        if file_name:
            try:
                if file_name.endswith('.csv'):
                    with open(file_name, 'r', newline='') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            group = row.get('group', self.current_group)
                            if group not in self.password_manager.list_groups():
                                self.password_manager.create_group(group)
                            self.password_manager.add_entry(
                                row['website'],
                                row['username'],
                                row['password'],
                                group
                            )
                elif file_name.endswith('.json'):
                    with open(file_name, 'r') as file:
                        data = json.load(file)
                        for entry in data:
                            group = entry.get('group', self.current_group)
                            if group not in self.password_manager.list_groups():
                                self.password_manager.create_group(group)
                            self.password_manager.add_entry(
                                entry['website'],
                                entry['username'],
                                entry['password'],
                                group
                            )
                
                self.refresh_groups()
                self.refresh_table()
                self.log_message(f"Senhas importadas de {file_name}")
                QMessageBox.information(self, "Sucesso", "Senhas importadas com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao importar senhas: {str(e)}")
                self.log_message(f"Erro ao importar senhas: {str(e)}")
    
    def export_passwords(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Senhas",
            "",
            "CSV Files (*.csv);;JSON Files (*.json)"
        )
        
        if file_name:
            try:
                all_entries = []
                for group, entries in self.password_manager.get_all_entries().items():
                    for website, data in entries.items():
                        entry = {
                            'group': group,
                            'website': website,
                            'username': data['username'],
                            'password': self.password_manager.get_password(website, group)
                        }
                        all_entries.append(entry)
                
                if file_name.endswith('.csv'):
                    with open(file_name, 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=['group', 'website', 'username', 'password'])
                        writer.writeheader()
                        for entry in all_entries:
                            writer.writerow(entry)
                elif file_name.endswith('.json'):
                    with open(file_name, 'w') as file:
                        json.dump(all_entries, file, indent=4)
                
                self.log_message(f"Senhas exportadas para {file_name}")
                QMessageBox.information(self, "Sucesso", "Senhas exportadas com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao exportar senhas: {str(e)}")
                self.log_message(f"Erro ao exportar senhas: {str(e)}")

    def copy_username(self, website: str):
        """Copiar usuário para a área de transferência."""
        try:
            entry = self.password_manager.get_entry(website, self.current_group)
            if entry:
                clipboard = QApplication.clipboard()
                clipboard.setText(entry["username"])
                self.log_message(f"Usuário copiado para {website}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            self.log_message(f"Erro ao copiar usuário: {str(e)}")

    def copy_password(self, website: str):
        """Copiar senha para a área de transferência."""
        try:
            password = self.password_manager.get_password(website, self.current_group)
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            self.log_message(f"Senha copiada para {website}")
            # Limpar a área de transferência após 30 segundos
            QTimer.singleShot(30000, lambda: clipboard.clear())
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            self.log_message(f"Erro ao copiar senha: {str(e)}")

    def truncate_text(self, text, max_length):
        """Trunca texto longo e adiciona ..."""
        if len(text) > max_length:
            return text[:max_length-3] + "..."
        return text

    def format_time_ago(self, timestamp):
        """Formata tempo relativo de forma amigável"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.total_seconds() < 60:
            return "Agora"
        elif diff.total_seconds() < 3600:
            minutes = int(diff.total_seconds() / 60)
            return f"Há {minutes}min"
        elif diff.days < 1:
            return timestamp.strftime("%H:%M")
        elif diff.days < 7:
            return timestamp.strftime("%a %H:%M")
        else:
            return timestamp.strftime("%d/%m/%y")

    def refresh_table(self):
        self.table.setRowCount(0)
        entries = self.password_manager.get_all_entries()[self.current_group]
        
        for website, data in entries.items():
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Website com ícone e link
            website_widget = QWidget()
            website_layout = QHBoxLayout(website_widget)
            website_layout.setContentsMargins(5, 0, 5, 0)
            website_layout.setSpacing(5)
            
            globe_icon = QLabel("🌐")
            website_label = QLabel(f'<a href="{website}" style="color: #2ecc71; text-decoration: none;">{self.truncate_text(website, 30)}</a>')
            website_label.setOpenExternalLinks(True)
            website_layout.addWidget(globe_icon)
            website_layout.addWidget(website_label)
            website_layout.addStretch()
            self.table.setCellWidget(row, 0, website_widget)
            
            # Username (truncado se necessário)
            username = self.truncate_text(data["username"], 25)
            username_item = QTableWidgetItem(username)
            username_item.setFlags(username_item.flags() & ~Qt.ItemIsEditable)
            username_item.setToolTip("Clique duplo para copiar")
            self.table.setItem(row, 1, username_item)
            
            # Password (hidden)
            password_widget = QWidget()
            password_layout = QHBoxLayout(password_widget)
            password_layout.setContentsMargins(5, 0, 5, 0)
            password_layout.setSpacing(5)
            
            lock_icon = QLabel("🔒")
            dots_label = QLabel("•••••••••••")
            dots_label.setAlignment(Qt.AlignCenter)
            password_layout.addWidget(lock_icon)
            password_layout.addWidget(dots_label, 1)
            self.table.setCellWidget(row, 2, password_widget)
            
            # Last modified (formato relativo)
            last_modified = datetime.fromtimestamp(data["last_modified"])
            modified_text = self.format_time_ago(last_modified)
            modified_item = QTableWidgetItem(modified_text)
            modified_item.setFlags(modified_item.flags() & ~Qt.ItemIsEditable)
            modified_item.setTextAlignment(Qt.AlignCenter)
            modified_item.setToolTip(last_modified.strftime("%d/%m/%Y %H:%M"))
            self.table.setItem(row, 3, modified_item)
            
            # Action buttons
            action_widget = QWidget()
            action_widget.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                }
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                    padding: 6px;
                    font-size: 18px;
                    min-width: 32px;
                    min-height: 32px;
                }
                QPushButton[primary="true"] {
                    color: #2ecc71;
                }
                QPushButton[primary="true"]:hover {
                    background-color: #2ecc7115;
                }
                QPushButton[secondary="true"] {
                    color: #27ae60;
                }
                QPushButton[secondary="true"]:hover {
                    background-color: #27ae6015;
                }
                QPushButton[tertiary="true"] {
                    color: #16a085;
                }
                QPushButton[tertiary="true"]:hover {
                    background-color: #16a08515;
                }
                QPushButton:pressed {
                    background-color: transparent;
                }
                QFrame.separator {
                    background-color: #404040;
                    width: 1px;
                    margin: 6px;
                }
            """)
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 0, 4, 0)
            action_layout.setSpacing(1)
            action_layout.setAlignment(Qt.AlignCenter)

            # Configuração dos grupos de botões
            buttons_config = [
                # Grupo 1: Ações Primárias
                [
                    ("👁", "Mostrar/Ocultar Senha (Alt+S)", self.show_password, "primary"),
                    ("🔑", "Copiar Senha (Alt+C)", self.copy_password, "primary"),
                    ("👤", "Copiar Usuário (Alt+U)", self.copy_username, "primary")
                ],
                # Grupo 2: Ações de Edição
                [
                    ("✏", "Editar Senha (Alt+E)", self.edit_entry, "secondary"),
                    ("🌐", "Abrir Website (Alt+W)", self.open_website, "secondary")
                ],
                # Grupo 3: Ações Secundárias
                [
                    ("📦", "Mover para Grupo (Alt+M)", self.move_entry, "tertiary"),
                    ("🗑", "Excluir Senha (Del)", self.delete_entry, "tertiary")
                ]
            ]

            # Adicionar os grupos de botões
            for i, group in enumerate(buttons_config):
                if i > 0:
                    # Separador visual entre grupos
                    separator = QFrame()
                    separator.setFrameShape(QFrame.VLine)
                    separator.setProperty("class", "separator")
                    action_layout.addWidget(separator)

                # Adicionar botões do grupo
                group_widget = QWidget()
                group_layout = QHBoxLayout(group_widget)
                group_layout.setContentsMargins(0, 0, 0, 0)
                group_layout.setSpacing(1)

                for icon_text, tooltip, callback, button_type in group:
                    btn = QPushButton(icon_text)
                    btn.setProperty(button_type, "true")
                    btn.setToolTip(tooltip)
                    btn.setToolTipDuration(2000)
                    btn.clicked.connect(lambda checked, w=website, c=callback: c(w))
                    btn.setCursor(Qt.PointingHandCursor)

                    # Estilo do tooltip
                    tooltip_style = """
                        QToolTip {
                            background-color: #2b2b2b;
                            color: #ffffff;
                            border: 1px solid #404040;
                            padding: 5px;
                            font-size: 11px;
                        }
                    """
                    btn.setStyleSheet(tooltip_style)
                    
                    group_layout.addWidget(btn)

                action_layout.addWidget(group_widget)

            self.table.setCellWidget(row, 4, action_widget)
        
        self.log_message("Tabela atualizada")

    def show_success_message(self, message):
        """Mostra uma mensagem de sucesso temporária"""
        self.log_message(message)
        
        # Criar widget de notificação
        notification = QLabel(message)
        notification.setStyleSheet("""
            QLabel {
                background-color: #2ecc71;
                color: #1b1b1b;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        notification.setAlignment(Qt.AlignCenter)
        
        # Adicionar ao layout principal
        main_layout = self.layout()
        main_layout.addWidget(notification)
        
        # Animar entrada
        animation = QPropertyAnimation(notification, b"opacity")
        animation.setDuration(200)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.start()
        
        # Remover após 2 segundos com animação
        def remove_notification():
            fade_out = QPropertyAnimation(notification, b"opacity")
            fade_out.setDuration(200)
            fade_out.setStartValue(1)
            fade_out.setEndValue(0)
            fade_out.finished.connect(notification.deleteLater)
            fade_out.start()
        
        QTimer.singleShot(1800, remove_notification)

class AddEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Nova Senha")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Website
        website_layout = QHBoxLayout()
        website_label = QLabel("Website:")
        self.website_input = QLineEdit()
        website_layout.addWidget(website_label)
        website_layout.addWidget(self.website_input)
        
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
        
        # Show password checkbox
        show_password = QPushButton("👁️")
        show_password.setCheckable(True)
        show_password.toggled.connect(
            lambda checked: self.password_input.setEchoMode(
                QLineEdit.Normal if checked else QLineEdit.Password
            )
        )
        password_layout.addWidget(show_password)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        # Add all layouts
        layout.addLayout(website_layout)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

class EditEntryDialog(QDialog):
    def __init__(self, website, username, password, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Senha")
        self.website = website
        self.username = username
        self.password = password
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Website
        website_layout = QHBoxLayout()
        website_label = QLabel("Website:")
        self.website_input = QLineEdit(self.website)
        website_layout.addWidget(website_label)
        website_layout.addWidget(self.website_input)
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Usuário:")
        self.username_input = QLineEdit(self.username)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Senha:")
        self.password_input = QLineEdit(self.password)
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Show password checkbox
        show_password = QPushButton("👁️")
        show_password.setCheckable(True)
        show_password.toggled.connect(
            lambda checked: self.password_input.setEchoMode(
                QLineEdit.Normal if checked else QLineEdit.Password
            )
        )
        password_layout.addWidget(show_password)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        # Add all layouts
        layout.addLayout(website_layout)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout) 