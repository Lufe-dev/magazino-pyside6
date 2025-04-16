from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QDateEdit,QScrollArea,QGroupBox,QMessageBox
from PySide6.QtWidgets import QTableWidgetItem, QPushButton, QVBoxLayout, QGroupBox, QTableWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QFormLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QDialogButtonBox, QVBoxLayout
from PySide6.QtCore import QTimer, Qt, QDate
from style import aplicar_estilo, configurar_botones
from db import Database

class Linea_Produccion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linea di produzione")
        self.showMaximized()
        aplicar_estilo(self)
        self.db = Database()
        self.layout = QVBoxLayout()

        # Campo de fecha con botones para sumar/restar días
        self.date_layout = QHBoxLayout()

        self.label = QLabel("Stato attuale della linea di produzione:")
        self.date_layout.addWidget(self.label)

        self.date_layout.addStretch(1)  # Espaciador

        self.label_data = QLabel("Seleziona la data:")
        self.date_layout.addWidget(self.label_data)

        self.boton_restar_dia = QPushButton("◀")
        self.boton_restar_dia.clicked.connect(self.restar_dia)
        configurar_botones([self.boton_restar_dia])
        self.date_layout.addWidget(self.boton_restar_dia)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.dateChanged.connect(self.actualizar_produccion)
        self.date_edit.setFixedWidth(120)
        aplicar_estilo(self.date_edit)
        self.date_layout.addWidget(self.date_edit)

        self.boton_sumar_dia = QPushButton("▶")
        self.boton_sumar_dia.clicked.connect(self.sumar_dia)
        configurar_botones([self.boton_sumar_dia])
        self.date_layout.addWidget(self.boton_sumar_dia)

        self.boton_restar_dia.setFixedHeight(29)
        self.boton_sumar_dia.setFixedHeight(29)

        self.layout.addLayout(self.date_layout)

        # Scroll area para las grillas de ortaggi
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Botón para actualizar manualmente
        self.boton_actualizar = QPushButton("Aggiornare")
        self.boton_actualizar.clicked.connect(self.actualizar_produccion)
        configurar_botones([self.boton_actualizar])
        self.layout.addWidget(self.boton_actualizar)

        self.setLayout(self.layout)

        # Temporizador para actualizar la tabla cada 5 minutos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_produccion)
        self.timer.start(300000)  # 5 minutos

        # Diccionario para almacenar las grillas
        self.grillas_ortaggi = {}

        # Cargar datos
        self.actualizar_produccion()

    def actualizar_produccion(self):
        """Obtiene y actualiza los datos agrupados por ortaggio."""
        fecha_filtrada = self.date_edit.date().toString("yyyy-MM-dd")

        query = """
        SELECT o.ortaggio_nome, 
            c.cliente_nome, 
            lp.colli, 
            l.lavorazione_nome, 
            i.imballaggio_nome, 
            p.pedana_nome, 
            s.stato_nome, 
            m.magazzino_nome,  -- Nuevo campo
            lp.info,           -- Nuevo campo Info
            lp.data
        FROM natura_test.linea_produzione lp
        LEFT JOIN natura_test.ortaggi o ON lp.ortaggio_key = o.ortaggio_key
        LEFT JOIN natura_test.clienti c ON lp.cliente_key = c.cliente_key
        LEFT JOIN natura_test.lavorazioni l ON lp.lavorazione_key = l.lavorazione_key
        LEFT JOIN natura_test.imballaggi i ON lp.imballaggio_key = i.imballaggio_key
        LEFT JOIN natura_test.pedane p ON lp.pedana_key = p.pedana_key
        LEFT JOIN natura_test.stati_ordine s ON lp.stato_key = s.stato_key
        LEFT JOIN natura_test.magazzini m ON lp.magazzino_key = m.magazzino_key  -- Nuevo
        WHERE lp.data = %s;
            
        """

        datos_filtrados = self.db.ejecutar_consulta(query, (fecha_filtrada,), fetch=True)

        # Organizar datos por ortaggio
        datos_por_ortaggio = {}
        for fila in datos_filtrados:
            ortaggio_nome = fila[0]  # Primer campo es el nombre del ortaggio
            if ortaggio_nome not in datos_por_ortaggio:
                datos_por_ortaggio[ortaggio_nome] = []
            datos_por_ortaggio[ortaggio_nome].append(fila)

        # Limpiar las tablas existentes
        for tabla in self.grillas_ortaggi.values():
            self.scroll_layout.removeWidget(tabla)
            tabla.deleteLater()
        self.grillas_ortaggi.clear()

        # Crear una tabla para cada ortaggio
        for ortaggio_nome, datos in datos_por_ortaggio.items():
            groupbox = QGroupBox(ortaggio_nome)  # Contenedor con título
            vbox = QVBoxLayout(groupbox)

            tabla = QTableWidget()
            tabla.setColumnCount(9)  # Ahora 9 columnas
            tabla.setHorizontalHeaderLabels([
                "Clienti", "Colli", "Lavorazione", "Imbalaggio", "Pedana", "Stato", 
                "Magazzino", "Info", "Data"  # Nuevas columnas agregadas
            ])
            tabla.setRowCount(len(datos))

            for fila, pedido in enumerate(datos):
                for columna, dato in enumerate(pedido[1:]):  # Saltamos el ortaggio
                    item = QTableWidgetItem(str(dato))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    tabla.setItem(fila, columna, item)

            # Ajustar diseño de tabla
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            vbox.addWidget(tabla)
            self.scroll_layout.addWidget(groupbox)
            self.grillas_ortaggi[ortaggio_nome] = groupbox

    def restar_dia(self):
        """Resta un día a la fecha seleccionada."""
        self.date_edit.setDate(self.date_edit.date().addDays(-1))

    def sumar_dia(self):
        """Suma un día a la fecha seleccionada."""
        self.date_edit.setDate(self.date_edit.date().addDays(1))



class Agregar_Linea_Produccion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aggiungi alla linea di produzione")
        self.db = Database()
        self.resize(450, 450)  # Aumenta el tamaño para encajar el nuevo campo
        aplicar_estilo(self)

        self.layout = QVBoxLayout()

        # Obtener datos con claves
        ortaggi = self.obtener_datos_desde_db("SELECT ortaggio_key, ortaggio_nome FROM natura_test.ortaggi")
        imballaggi = self.obtener_datos_desde_db("SELECT imballaggio_key, imballaggio_nome FROM natura_test.imballaggi")
        pedane = self.obtener_datos_desde_db("SELECT pedana_key, pedana_nome FROM natura_test.pedane")
        clienti = self.obtener_datos_desde_db("SELECT cliente_key, cliente_nome FROM natura_test.clienti")
        stati_ordine = self.obtener_datos_desde_db("SELECT stato_key, stato_nome FROM natura_test.stati_ordine")
        magazzini = self.obtener_datos_desde_db("SELECT magazzino_key, magazzino_nome FROM natura_test.magazzini")  # Nuevo

        # Crear los combobox con claves y nombres
        self._agregar_combox("Seleziona un Ortaggio:", ortaggi, "combobox_Ortaggi", self.actualizar_lavorazioni)
        self._agregar_combox("Seleziona un Imbalaggio:", imballaggi, "combobox_Imbalaggio")
        self._agregar_combox("Seleziona la Pedana:", pedane, "combobox_Pedana")
        self._agregar_combox("Seleziona un Cliente:", clienti, "combobox_Clienti")
        self._agregar_combox("Seleziona lo Stato dell'ordine:", stati_ordine, "combobox_stati_ordine")
        self._agregar_combox("Seleziona un Magazzino:", magazzini, "combobox_Magazzini")  # Nuevo

        # Combobox de Lavorazioni (se llenará dinámicamente)
        self._agregar_combox("Seleziona una Lavorazione:", [], "combobox_Lavorazioni")

        # Layout para Colli y Fecha
        self.date_colli = QHBoxLayout()

        self.label_colli = QLabel("Inserisci il numero di Colli:")
        self.date_colli.addWidget(self.label_colli)

        self.text_colli = QLineEdit()
        aplicar_estilo(self.text_colli)
        self.date_colli.addWidget(self.text_colli)

        self.label_data = QLabel("Seleziona la Data:")
        self.date_colli.addWidget(self.label_data)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        aplicar_estilo(self.date_edit)
        self.date_colli.addWidget(self.date_edit)

        self.layout.addLayout(self.date_colli)

        # Agregar el campo de texto para "Info"
        self.label_info = QLabel("Info:")
        self.layout.addWidget(self.label_info)

        self.text_info = QLineEdit()
        aplicar_estilo(self.text_info)
        self.layout.addWidget(self.text_info)

        # Espaciador vertical
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Mensaje y Botón
        self.label_mensaje = QLabel("")
        aplicar_estilo(self.label_mensaje)
        self.layout.addWidget(self.label_mensaje)

        self.boton_agregar = QPushButton("Aggiungi")
        self.boton_agregar.clicked.connect(self.agregar)
        configurar_botones([self.boton_agregar])
        self.layout.addWidget(self.boton_agregar)

        self.setLayout(self.layout)
    def _agregar_combox(self, label_text, items, attr_name, on_change=None):
        """Crea un QLabel y un QComboBox, los llena con `items` (clave, nombre) y los guarda como atributo."""
        label = QLabel(label_text)
        self.layout.addWidget(label)

        combobox = QComboBox()
        for key, name in items:
            combobox.addItem(name, key)  # Almacena la clave en QVariant
        
        aplicar_estilo(combobox)
        self.layout.addWidget(combobox)

        if on_change:
            combobox.currentIndexChanged.connect(on_change)

        setattr(self, attr_name, combobox)

        self.layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

    def obtener_datos_desde_db(self, query, params=None):
        """Ejecuta una consulta SQL y devuelve una lista de tuplas (clave, nombre)."""
        return self.db.ejecutar_consulta(query, params if params else (), fetch=True)

    def actualizar_lavorazioni(self):
        """Actualiza el combobox de Lavorazioni basado en el Ortaggio seleccionado."""
        ortaggio_key = self.combobox_Ortaggi.currentData()

        if ortaggio_key is None:
            return

        query_lavorazioni = """
            SELECT l.lavorazione_key, l.lavorazione_nome 
            FROM natura_test.lavorazioni l
            JOIN natura_test.lavorazione_ortaggi lo ON l.lavorazione_key = lo.lavorazione_key
            WHERE lo.ortaggio_key = %s
        """
        lavorazioni_filtrate = self.obtener_datos_desde_db(query_lavorazioni, (ortaggio_key,))

        self.combobox_Lavorazioni.clear()
        for key, name in lavorazioni_filtrate:
            self.combobox_Lavorazioni.addItem(name, key)

    def agregar(self):
        """Inserta la línea de producción con claves en lugar de nombres."""
        ortaggio_key = self.combobox_Ortaggi.currentData()
        imballaggio_key = self.combobox_Imbalaggio.currentData()
        pedana_key = self.combobox_Pedana.currentData()
        cliente_key = self.combobox_Clienti.currentData()
        stato_key = self.combobox_stati_ordine.currentData()
        lavorazione_key = self.combobox_Lavorazioni.currentData()
        magazzino_key = self.combobox_Magazzini.currentData()  # Nuevo
        colli = self.text_colli.text()
        info = self.text_info.text()  # Obtener el texto del campo de info

        def calcular_colli(colli_text):
            if "x" in colli_text:  # Caso multiplicación (30x40)
                partes = colli_text.split("x")
                try:
                    return int(partes[0]) * int(partes[1])
                except ValueError:
                    return None
            elif "+" in colli_text:  # Caso suma (80+20)
                partes = colli_text.split("+")
                try:
                    return sum(int(x) for x in partes)
                except ValueError:
                    return None
            else:  # Caso normal (50)
                try:
                    return int(colli_text)
                except ValueError:
                    return None
        colli_num = calcular_colli(colli)
        data = self.date_edit.date().toString("yyyy-MM-dd")  # Formato compatible con PostgreSQL

        # Verificar que todos los campos están completos
        if all([ortaggio_key, imballaggio_key, pedana_key, cliente_key, stato_key, lavorazione_key, magazzino_key, colli, colli_num, data, info]):
            query = """
                INSERT INTO natura_test.linea_produzione 
                (ortaggio_key, imballaggio_key, pedana_key, cliente_key, stato_key, colli, colli_num, data, lavorazione_key, magazzino_key, info)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (ortaggio_key, imballaggio_key, pedana_key, cliente_key, stato_key, colli, colli_num, data, lavorazione_key, magazzino_key, info)

            # Ejecutar la inserción en la base de datos
            self.db.ejecutar_consulta(query, params)

            # Mostrar mensaje de éxito
            self.label_mensaje.setText(f"Ortaggio '{self.combobox_Ortaggi.currentText()}' aggiunto alla linea di produzione.")

            # Limpiar el campo de colli y el campo de info
            self.text_colli.clear()
            self.text_info.clear()

            # Hacer que el mensaje desaparezca después de 5 segundos
            QTimer.singleShot(5000, self.limpiar_mensaje)

        else:
            self.label_mensaje.setText("Errore: tutti i campi devono essere compilati.")
            
            # Limpiar los campos
            self.text_colli.clear()
            self.text_info.clear()

            # Hacer que el mensaje desaparezca después de 5 segundos
            QTimer.singleShot(5000, self.limpiar_mensaje)

    def limpiar_mensaje(self):
        """Limpia el mensaje de la label."""
        self.label_mensaje.clear()


class Modificar_Orden(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linea di produzione")
        self.showMaximized()
        aplicar_estilo(self)
        self.db = Database()
        self.layout = QVBoxLayout()

      
        # Campo de fecha con botones para sumar/restar días
        self.date_layout = QHBoxLayout()

        self.label = QLabel("Stato attuale della linea di produzione:")
        self.date_layout.addWidget(self.label)

        self.date_layout.addStretch(1)  # Espaciador

        self.label_data = QLabel("Seleziona la data:")
        self.date_layout.addWidget(self.label_data)

        self.boton_restar_dia = QPushButton("◀")
        self.boton_restar_dia.clicked.connect(self.restar_dia)
        configurar_botones([self.boton_restar_dia])
        self.date_layout.addWidget(self.boton_restar_dia)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.dateChanged.connect(self.actualizar_produccion)
        self.date_edit.setFixedWidth(120)
        aplicar_estilo(self.date_edit)
        self.date_layout.addWidget(self.date_edit)

        self.boton_sumar_dia = QPushButton("▶")
        self.boton_sumar_dia.clicked.connect(self.sumar_dia)
        configurar_botones([self.boton_sumar_dia])
        self.date_layout.addWidget(self.boton_sumar_dia)

        self.boton_restar_dia.setFixedHeight(29)
        self.boton_sumar_dia.setFixedHeight(29)

        self.layout.addLayout(self.date_layout)

        # Scroll area para las grillas de ortaggi
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Botón para actualizar manualmente
        self.boton_actualizar = QPushButton("Aggiornare")
        self.boton_actualizar.clicked.connect(self.actualizar_produccion)
        configurar_botones([self.boton_actualizar])
        self.layout.addWidget(self.boton_actualizar)

        self.setLayout(self.layout)

        # Temporizador para actualizar la tabla cada 5 minutos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_produccion)
        self.timer.start(300000)  # 5 minutos

        # Diccionario para almacenar las grillas
        self.grillas_ortaggi = {}

        # Cargar datos
        self.actualizar_produccion()

    def actualizar_produccion(self):
        """Obtiene y actualiza los datos agrupados por ortaggio."""
        fecha_filtrada = self.date_edit.date().toString("yyyy-MM-dd")

        query = """
        SELECT o.ortaggio_nome, 
            c.cliente_nome, 
            lp.colli, 
            l.lavorazione_nome, 
            i.imballaggio_nome, 
            p.pedana_nome, 
            s.stato_nome, 
            m.magazzino_nome,  
            lp.info,           
            lp.data, 
            lp.linea_produzione_key  -- Se agrega el ID de la línea de producción para eliminar y modificar
        FROM natura_test.linea_produzione lp
        LEFT JOIN natura_test.ortaggi o ON lp.ortaggio_key = o.ortaggio_key
        LEFT JOIN natura_test.clienti c ON lp.cliente_key = c.cliente_key
        LEFT JOIN natura_test.lavorazioni l ON lp.lavorazione_key = l.lavorazione_key
        LEFT JOIN natura_test.imballaggi i ON lp.imballaggio_key = i.imballaggio_key
        LEFT JOIN natura_test.pedane p ON lp.pedana_key = p.pedana_key
        LEFT JOIN natura_test.stati_ordine s ON lp.stato_key = s.stato_key
        LEFT JOIN natura_test.magazzini m ON lp.magazzino_key = m.magazzino_key  
        WHERE lp.data = %s;
        """
        datos_filtrados = self.db.ejecutar_consulta(query, (fecha_filtrada,), fetch=True)

        # Organizar datos por ortaggio
        datos_por_ortaggio = {}
        for fila in datos_filtrados:
            ortaggio_nome = fila[0]
            if ortaggio_nome not in datos_por_ortaggio:
                datos_por_ortaggio[ortaggio_nome] = []
            datos_por_ortaggio[ortaggio_nome].append(fila)

        # Limpiar las tablas existentes
        for tabla in self.grillas_ortaggi.values():
            self.scroll_layout.removeWidget(tabla)
            tabla.deleteLater()
        self.grillas_ortaggi.clear()

        # Crear una tabla para cada ortaggio
        for ortaggio_nome, datos in datos_por_ortaggio.items():
            groupbox = QGroupBox(ortaggio_nome)  # Contenedor con título
            vbox = QVBoxLayout(groupbox)

            tabla = QTableWidget()
            tabla.setColumnCount(11)  # Añadir 2 columnas más para los botones
            tabla.setHorizontalHeaderLabels([
                "Clienti", "Colli", "Lavorazione", "Imbalaggio", "Pedana", "Stato", 
                "Magazzino", "Info", "Data", "", ""
            ])
            tabla.setRowCount(len(datos))

            for fila, pedido in enumerate(datos):
                for columna, dato in enumerate(pedido[1:-1]):  # Excluimos el ortaggio y la key
                    item = QTableWidgetItem(str(dato))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    tabla.setItem(fila, columna, item)

                # Añadir botones de Modificar y Eliminar
                modificar_btn = QPushButton("Modificare")
                modificar_btn.clicked.connect(lambda checked, id=pedido[-1]: self.modificar_orden(id))  # Usar el ID de la línea de producción
                eliminar_btn = QPushButton("Elimina")
                eliminar_btn.clicked.connect(lambda checked, id=pedido[-1]: self.eliminar_orden(id))

                tabla.setCellWidget(fila, 9, modificar_btn)
                tabla.setCellWidget(fila, 10, eliminar_btn)

            # Ajustar diseño de tabla
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            vbox.addWidget(tabla)
            self.scroll_layout.addWidget(groupbox)
            self.grillas_ortaggi[ortaggio_nome] = groupbox

    def modificar_orden(self, orden_id):
        """Abre la ventana para modificar la orden."""
        # Crear una nueva ventana para modificar la orden
        dialogo_modificar = ModificarOrdenDialog(orden_id)
        dialogo_modificar.exec()

    def eliminar_orden(self, orden_id):
        """Pregunta si está seguro de eliminar la orden."""
        confirmacion = QMessageBox.question(self, "Conferma", "Sei sicuro di rimuovere questo ordine?", 
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmacion == QMessageBox.Yes:
            query = "DELETE FROM natura_test.linea_produzione WHERE linea_produzione_key = %s"
            self.db.ejecutar_consulta(query, (orden_id,))
            self.actualizar_produccion()  # Actualiza la vista después de eliminar
    def restar_dia(self):
        """Resta un día a la fecha seleccionada."""
        self.date_edit.setDate(self.date_edit.date().addDays(-1))

    def sumar_dia(self):
        """Suma un día a la fecha seleccionada."""
        self.date_edit.setDate(self.date_edit.date().addDays(1))

        
class ModificarOrdenDialog(QDialog):
    def __init__(self, orden_id):
        super().__init__()
        self.resize(450, 450)  
        self.setWindowTitle("Modifica ordine")
        
        # Asignar el ID de la orden
        self.orden_id = orden_id  # Aquí se asigna correctamente el orden_id al objeto
        self.db = Database()
        aplicar_estilo(self)

        self.layout = QFormLayout()

        # Obtener datos de la base de datos
        clienti = self.obtener_datos_desde_db("SELECT cliente_key, cliente_nome FROM natura_test.clienti")
        ortaggi = self.obtener_datos_desde_db("SELECT ortaggio_key, ortaggio_nome FROM natura_test.ortaggi")
        lavorazioni = self.obtener_datos_desde_db("SELECT lavorazione_key, lavorazione_nome FROM natura_test.lavorazioni")
        imballaggi = self.obtener_datos_desde_db("SELECT imballaggio_key, imballaggio_nome FROM natura_test.imballaggi")
        pedane = self.obtener_datos_desde_db("SELECT pedana_key, pedana_nome FROM natura_test.pedane")
        stati_ordine = self.obtener_datos_desde_db("SELECT stato_key, stato_nome FROM natura_test.stati_ordine")
        magazzini = self.obtener_datos_desde_db("SELECT magazzino_key, magazzino_nome FROM natura_test.magazzini")

        # Crear los combobox con claves y nombres
        self._agregar_combox("Seleziona un Ortaggio:", ortaggi, "combobox_Ortaggi", self.actualizar_lavorazioni)
        self._agregar_combox("Seleziona un Imbalaggio:", imballaggi, "combobox_Imbalaggio")
        self._agregar_combox("Seleziona la Pedana:", pedane, "combobox_Pedana")
        self._agregar_combox("Seleziona un Cliente:", clienti, "combobox_Clienti")
        self._agregar_combox("Seleziona lo Stato dell'ordine:", stati_ordine, "combobox_stati_ordine")
        self._agregar_combox("Seleziona un Magazzino:", magazzini, "combobox_Magazzini")  # Nuevo

        # Combobox de Lavorazioni (se llenará dinámicamente)
        self._agregar_combox("Seleziona una Lavorazione:", [], "combobox_Lavorazioni")
        # Layout para Colli y Fecha
        self.date_colli = QHBoxLayout()

        self.label_colli = QLabel("Inserisci il numero di Colli:")
        self.date_colli.addWidget(self.label_colli)

        self.text_colli = QLineEdit()
        aplicar_estilo(self.text_colli)
        self.date_colli.addWidget(self.text_colli)

        self.label_data = QLabel("Seleziona la Data:")
        self.date_colli.addWidget(self.label_data)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        aplicar_estilo(self.date_edit)
        self.date_colli.addWidget(self.date_edit)

        # Crear un contenedor QWidget para el QHBoxLayout
        contenedor_date_colli = QWidget()
        contenedor_date_colli.setLayout(self.date_colli)

        # Agregar el contenedor al QFormLayout usando addRow()
        self.layout.addRow(contenedor_date_colli)

        # Agregar el campo de texto para "Info"
        self.label_info = QLabel("Info:")
        self.layout.addWidget(self.label_info)

        self.text_info = QLineEdit()
        aplicar_estilo(self.text_info)
        self.layout.addWidget(self.text_info)

        # Espaciador vertical
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Cargar los datos de la orden seleccionada
        self.cargar_datos_orden()

        # Botón para guardar cambios
        self.boton_guardar = QPushButton("Salva modifiche")
        self.boton_guardar.clicked.connect(self.guardar_cambios)
        self.layout.addWidget(self.boton_guardar)

        self.setLayout(self.layout)

    def cargar_datos_orden(self):
        """Carga los datos de la orden seleccionada y actualiza los campos y comboboxes."""
        if not hasattr(self, 'orden_id'):
            print("Errore: id_order non è definito.")
            return
        
        query = "SELECT * FROM natura_test.linea_produzione WHERE linea_produzione_key = %s;"
        orden_data = self.db.ejecutar_consulta(query, (self.orden_id,), fetch=True, como_diccionario=True)

        if orden_data:
            orden = orden_data[0]

            # Preseleccionar valores en los comboboxes
            self.combobox_Clienti.setCurrentIndex(self.combobox_Clienti.findData(orden['cliente_key']))
            self.combobox_Ortaggi.setCurrentIndex(self.combobox_Ortaggi.findData(orden['ortaggio_key']))
            self.combobox_Lavorazioni.setCurrentIndex(self.combobox_Lavorazioni.findData(orden['lavorazione_key']))
            self.combobox_Imbalaggio.setCurrentIndex(self.combobox_Imbalaggio.findData(orden['imballaggio_key']))
            self.combobox_Pedana.setCurrentIndex(self.combobox_Pedana.findData(orden['pedana_key']))
            self.combobox_stati_ordine.setCurrentIndex(self.combobox_stati_ordine.findData(orden['stato_key']))
            self.combobox_Magazzini.setCurrentIndex(self.combobox_Magazzini.findData(orden['magazzino_key']))

            # Rellenar los campos de texto
            self.text_colli.setText(str(orden['colli']))
            self.text_info.setText(orden['info'])

            # Establecer la fecha
            fecha = QDate.fromString(str(orden['data']), "yyyy-MM-dd")
            self.date_edit.setDate(fecha if fecha.isValid() else QDate.currentDate())
        else:
            print("L'ordine non è stato trovato.")
    def _agregar_combox(self, label_text, items, attr_name, on_changed=None):
        """Crea un QLabel y un QComboBox, los llena con `items` (clave, nombre) y los guarda como atributo.
        Si se proporciona, conecta una función al evento currentIndexChanged del combobox."""
        
        label = QLabel(label_text)
        self.layout.addRow(label)  # Usar addRow para agregar el QLabel

        combobox = QComboBox()
        for key, name in items:
            combobox.addItem(name, key)  # Almacena la clave en QVariant

        aplicar_estilo(combobox)
        self.layout.addRow(combobox)  # Usar addRow para agregar el QComboBox

        # Conectar la función 'on_changed' si se proporciona
        if on_changed:
            combobox.currentIndexChanged.connect(on_changed)

        setattr(self, attr_name, combobox)

        # Espaciador entre elementos
        espaciador = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout.addItem(espaciador)  # Agregar espaciador correctamente


    def obtener_datos_desde_db(self, query, params=None):
        """Ejecuta una consulta SQL y devuelve una lista de tuplas (clave, nombre)."""
        resultados = self.db.ejecutar_consulta(query, params if params else (), fetch=True, como_diccionario=True)

        if resultados and isinstance(resultados, list):
            primera_fila = resultados[0]
            if len(primera_fila) >= 2:
                claves, nombres = list(primera_fila.keys())[:2]  # Obtiene los primeros dos nombres de columna
                return [(fila[claves], fila[nombres]) for fila in resultados]  # Retorna clave y nombre real
            
        return []
    
    def actualizar_lavorazioni(self):
        """Actualiza el combobox de Lavorazioni basado en el Ortaggio seleccionado."""
        ortaggio_key = self.combobox_Ortaggi.currentData()

        if ortaggio_key is None:
            return

        query_lavorazioni = """
            SELECT l.lavorazione_key, l.lavorazione_nome 
            FROM natura_test.lavorazioni l
            JOIN natura_test.lavorazione_ortaggi lo ON l.lavorazione_key = lo.lavorazione_key
            WHERE lo.ortaggio_key = %s
        """
        lavorazioni_filtrate = self.obtener_datos_desde_db(query_lavorazioni, (ortaggio_key,))

        self.combobox_Lavorazioni.clear()
        for key, name in lavorazioni_filtrate:
            self.combobox_Lavorazioni.addItem(name, key)


    def guardar_cambios(self):
        """Actualiza una línea de producción con los datos modificados."""
        ortaggio_key = self.combobox_Ortaggi.currentData()
        imballaggio_key = self.combobox_Imbalaggio.currentData()
        pedana_key = self.combobox_Pedana.currentData()
        cliente_key = self.combobox_Clienti.currentData()
        stato_key = self.combobox_stati_ordine.currentData()
        lavorazione_key = self.combobox_Lavorazioni.currentData()
        magazzino_key = self.combobox_Magazzini.currentData()
        colli = self.text_colli.text()
        info = self.text_info.text()
        data = self.date_edit.date().toString("yyyy-MM-dd")  # Formato compatible con PostgreSQL

        def calcular_colli(colli_text):
            if "x" in colli_text:  
                partes = colli_text.split("x")
                try:
                    return int(partes[0]) * int(partes[1])
                except ValueError:
                    return None
            elif "+" in colli_text:  
                partes = colli_text.split("+")
                try:
                    return sum(int(x) for x in partes)
                except ValueError:
                    return None
            else:  
                try:
                    return int(colli_text)
                except ValueError:
                    return None

        colli_num = calcular_colli(colli)

        if all([ortaggio_key, imballaggio_key, pedana_key, cliente_key, stato_key, lavorazione_key, magazzino_key, colli, colli_num, data, info]):
            query = """
                UPDATE natura_test.linea_produzione
                SET ortaggio_key = %s, imballaggio_key = %s, pedana_key = %s, cliente_key = %s, stato_key = %s, 
                    colli = %s, colli_num = %s, data = %s, lavorazione_key = %s, magazzino_key = %s, info = %s
                WHERE linea_produzione_key = %s
            """
            params = (ortaggio_key, imballaggio_key, pedana_key, cliente_key, stato_key, 
                    colli, colli_num, data, lavorazione_key, magazzino_key, info, self.orden_id)

            self.db.ejecutar_consulta(query, params)

            # Mostrar mensaje emergente
            self.mostrar_mensaje("Modifica salvata con successo!", True)

        else:
            # Si hay algún campo vacío, mostramos el mensaje de error
            self.mostrar_mensaje("Errore: tutti i campi devono essere compilati.", False)

    def mostrar_mensaje(self, mensaje, exito):
        """Muestra un mensaje en una ventana emergente y cierra la ventana actual si es exitoso."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information if exito else QMessageBox.Critical)
        msg_box.setText(mensaje)
        msg_box.setWindowTitle("informazione")
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Conectar el evento de clic en "OK" para cerrar el diálogo
        msg_box.buttonClicked.connect(self.cerrar_ventana)

        msg_box.exec_()

    def cerrar_ventana(self, button):
        """Cierra la ventana actual después de mostrar el mensaje."""
        self.accept()
