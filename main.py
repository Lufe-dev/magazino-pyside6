from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGraphicsOpacityEffect, QMenu, QMenuBar, QApplication
from PySide6.QtGui import QAction, QPixmap, QIcon, QPainter, QBrush
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation
from abm_elements import abrir_abm, abm_lavorazione
from production import Linea_Produccion, Agregar_Linea_Produccion, Modificar_Orden
from style import aplicar_estilo_menu
import psycopg2
from psycopg2 import sql
from db import Database

db = Database()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Gestione della produzione di Ortaggi")


        # Establecer icono de la aplicación
        icon_path = r"C:\Python\magazino - pyside\images\favicon.png"
        self.setWindowIcon(QIcon(icon_path))


        # Establecer fondo blanco
        self.setStyleSheet("background-color: white;")
        # Crear un QLabel para la imagen de fondo
        self.background_label = QLabel(self)
        self.pixmap = QPixmap(icon_path)  # Cargar imagen
        self.background_label.setPixmap(self.pixmap)
        self.background_label.setAlignment(Qt.AlignCenter)  # Centrar la imagen sin escalar
        self.background_label.setScaledContents(False)  # No escalar la imagen
        self.setCentralWidget(self.background_label)

        # Crear efecto de opacidad para el desvanecimiento
        self.opacity_effect = QGraphicsOpacityEffect(self.background_label)
        self.background_label.setGraphicsEffect(self.opacity_effect)

        # Animación de desvanecimiento
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(3000)  # Duración de 5 segundos
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()


        # Ajustar la posición de la imagen en la ventana
        self.update_background_position()
        self.resizeEvent = self.update_background_position  # Actualizar al redimensionar

        # Crear los menús
        self.menu_abm = self.menuBar().addMenu("Iniziare")
        self.menu_produccion = self.menuBar().addMenu("Produzione")

        # Crear las acciones para el menú ABM y conectarlas a sus respectivas funciones
        action_Ortaggi = QAction("Ortaggi", self)
        action_Ortaggi.triggered.connect(self.abrir_abm_Ortaggi)
        self.menu_abm.addAction(action_Ortaggi)

        action_cajas = QAction("Imballaggio", self)
        action_cajas.triggered.connect(self.abrir_abm_cajas)
        self.menu_abm.addAction(action_cajas)

        action_pallets = QAction("Pedana", self)
        action_pallets.triggered.connect(self.abrir_abm_pallets)
        self.menu_abm.addAction(action_pallets)

        action_proveedores = QAction("Clienti", self)
        action_proveedores.triggered.connect(self.abrir_abm_proveedores)
        self.menu_abm.addAction(action_proveedores)

        action_estados = QAction("Stati dell'ordine", self)
        action_estados.triggered.connect(self.abrir_abm_estados)
        self.menu_abm.addAction(action_estados)

        action_lavorazione = QAction("Lavorazione", self)
        action_lavorazione.triggered.connect(self.abrir_abm_lavorazione)
        self.menu_abm.addAction(action_lavorazione)

        action_magazzini = QAction("Magazzini", self)
        action_magazzini.triggered.connect(self.abrir_abm_Magazzini)
        self.menu_abm.addAction(action_magazzini)

        # Agregar acciones a "Producción"
        action_ver_linea = QAction("Vedi la Linea di Produzione", self)
        action_ver_linea.triggered.connect(self.ver_linea_produccion)
        self.menu_produccion.addAction(action_ver_linea)

        action_agregar_linea = QAction("Aggiungere alla Linea di Produzione", self)
        action_agregar_linea.triggered.connect(self.agregar_a_linea_produccion)
        self.menu_produccion.addAction(action_agregar_linea)

        action_modificar_linea = QAction("Modifica l'ordine della linea di produzione", self)
        action_modificar_linea.triggered.connect(self.modificar_linea_produccion)
        self.menu_produccion.addAction(action_modificar_linea)


        self.showMaximized()  # Iniciar la aplicación maximizada

        # Aplicar estilo a los menús
        menu_bar = self.menuBar() 
        aplicar_estilo_menu(menu_bar)


    def update_background_position(self, event=None):
        if not self.pixmap.isNull():
            win_size = self.size()
            img_size = self.pixmap.size()
            x = (win_size.width() - img_size.width()) // 2
            y = (win_size.height() - img_size.height()) // 2
            self.background_label.setGeometry(QRect(x, y, img_size.width(), img_size.height()))

    def abrir_abm_Ortaggi(self):
        abrir_abm("ortaggi", "ortaggio_nome")  # Cambiar Ortaggio a "OrtoggioNome"

    def abrir_abm_Magazzini(self):
        abrir_abm("magazzini", "magazzino_nome")  # Cambiar Ortaggio a "OrtoggioNome"

    def abrir_abm_cajas(self):
        abrir_abm("imballaggi", "imballaggio_nome")  # Cambiar Imbalaggio a "ImballaggioNome"

    def abrir_abm_pallets(self):
        abrir_abm("pedane", "pedana_nome")  # Cambiar Pedana a "PedanaNome"

    def abrir_abm_proveedores(self):
        abrir_abm("clienti", "cliente_nome")  # Cambiar Clienti a "ClienteNome"

    def abrir_abm_estados(self):
        abrir_abm("stati_ordine", "stato_nome")  # Cambiar StatiOrdine a "StatoNome"

    def abrir_abm_lavorazione(self):
        abm_lavorazione()  # Cambiar Lavorazione a "LavorazioneNome"



    def ver_linea_produccion(self):
        self.ventana_produccion = Linea_Produccion()
        self.ventana_produccion.show()

    def agregar_a_linea_produccion(self):
        self.ventana_agregar = Agregar_Linea_Produccion()
        self.ventana_agregar.show()


    def modificar_linea_produccion(self):
        self.ventana_modificar = Modificar_Orden()
        self.ventana_modificar.show()

def main():
    app = QApplication([])
    app.setStyle("Fusion")  # Usar el estilo Fusion para la aplicación completa

    app.setWindowIcon(QIcon(r"C:\Python\magazino - pyside\images\favicon.png"))  # Establecer icono en la barra de tareas
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
