import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFont
from ui.password_widget import PasswordWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SecureVault - Gerenciador de Senhas")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #232323;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #44ff44;
                border: none;
                border-radius: 4px;
                padding: 4px;
                margin: 8px;
                color: #232323;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                background-color: #333333;
                color: #e0e0e0;
                border: 1px solid #44ff44;
                border-radius: 4px;
                padding: 4px;
                margin: 4px;
            }
            QTableWidget {
                background-color: #333333;
                color: #e0e0e0;
                border: 1px solid #44ff44;
                border-radius: 4px;
                gridline-color: #44ff44;
            }
            QHeaderView::section {
                background-color: #232323;
                color: #e0e0e0;
                border: 1px solid #44ff44;
                padding: 4px;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QSplitter::handle {
                background-color: #44ff44;
            }
            QSplitter::handle:horizontal {
                width: 4px;
            }
            QSplitter::handle:vertical {
                height: 4px;
            }
        """)
        
        # Set default font
        app = QApplication.instance()
        app.setFont(QFont("Segoe UI", 10))
        
        # Create and set the central widget
        self.password_widget = PasswordWidget()
        self.setCentralWidget(self.password_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 700)  # Aumentado a altura para acomodar o painel de log
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 