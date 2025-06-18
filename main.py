import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from ui.password_widget import PasswordWidget
from core.config import Config

def set_dark_theme(app):
    # Configurar o tema escuro
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#232323"))
    palette.setColor(QPalette.WindowText, QColor("#e0e0e0"))
    palette.setColor(QPalette.Base, QColor("#333333"))
    palette.setColor(QPalette.AlternateBase, QColor("#2b2b2b"))
    palette.setColor(QPalette.ToolTipBase, QColor("#333333"))
    palette.setColor(QPalette.ToolTipText, QColor("#e0e0e0"))
    palette.setColor(QPalette.Text, QColor("#e0e0e0"))
    palette.setColor(QPalette.Button, QColor("#232323"))
    palette.setColor(QPalette.ButtonText, QColor("#e0e0e0"))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor("#2ecc71"))
    palette.setColor(QPalette.Highlight, QColor("#2ecc71"))
    palette.setColor(QPalette.HighlightedText, QColor("#232323"))
    app.setPalette(palette)
    
    # Definir estilo global
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #232323;
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #2ecc71;
            color: #232323;
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #27ae60;
        }
        QLineEdit {
            padding: 5px;
            border: 1px solid #2ecc71;
            border-radius: 3px;
            background-color: #333333;
            color: #e0e0e0;
        }
        QTableWidget {
            border: 1px solid #2ecc71;
            border-radius: 3px;
            background-color: #333333;
            gridline-color: #2b2b2b;
        }
        QHeaderView::section {
            background-color: #232323;
            color: #e0e0e0;
            padding: 5px;
            border: 1px solid #2ecc71;
        }
        QScrollBar:vertical {
            border: none;
            background-color: #232323;
            width: 10px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background-color: #2ecc71;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QTextEdit {
            background-color: #333333;
            color: #44ff44;
            border: none;
            font-family: Consolas;
        }
    """)

def main():
    app = QApplication(sys.argv)
    
    # Initialize configuration
    config = Config()
    
    # Definir o ícone do aplicativo
    icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'images', 'securevault.ico')
    if not os.path.exists(icon_path):
        icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'images', 'securevault.png')
    
    app.setWindowIcon(QIcon(icon_path))
    
    # Configurar fonte padrão
    app.setFont(QFont("Segoe UI", 10))
    
    # Aplicar tema escuro e estilos
    set_dark_theme(app)
    
    # Criar e exibir a janela principal
    window = PasswordWidget(config)
    window.setWindowTitle("SecureVault")
    window.setWindowIcon(QIcon(icon_path))
    window.resize(900, 600)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 