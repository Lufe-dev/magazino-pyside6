from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPalette, QColor

def aplicar_estilo(widget: QWidget):
    # Creamos una paleta de colores oscura
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))  # Fondo oscuro
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # Texto blanco
    palette.setColor(QPalette.Button, QColor(50, 50, 50))  # Botones con fondo oscuro
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # Texto en botones blanco

    # Aplicamos la paleta al widget específico
    widget.setPalette(palette)
    
def configurar_botones(botones):
    for boton in botones:
        boton.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-size: 12pt;
            font-weight: bold;
            padding: 10px 15px;
        """)

def aplicar_estilo_menu(menu_bar):
    menu_bar.setStyleSheet("""
        QMenuBar {
            background-color: #4CAF50;
            color: white;
        }
        QMenuBar::item {
            background-color: #4CAF50;
            color: white;
        }
        QMenuBar::item:selected {
            background-color: #45a049;
        }
        QMenu {
            background-color: #4CAF50;
            color: white;
        }
        QMenu::item {
            background-color: #4CAF50;
            color: white;
        }
        QMenu::item:selected {
            background-color: #45a049;
        }
    """)