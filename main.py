import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.password_widget import PasswordWidget

def main():
    app = QApplication(sys.argv)
    
    # Definir o ícone do aplicativo
    icon_path = os.path.join('resources', 'images', 'securevault.ico')
    app.setWindowIcon(QIcon(icon_path))
    
    # Configurar o estilo da aplicação
    app.setStyle('Fusion')
    
    # Criar e exibir a janela principal
    window = PasswordWidget()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 