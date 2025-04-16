from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
    QCheckBox,QScrollArea, QListWidget, QPushButton, QMessageBox, QScrollArea, QGridLayout,
    QWidget, QVBoxLayout, QCheckBox, QPushButton, QMessageBox, QSizePolicy)
from db import Database  

# Crear instancia de la base de datos
db = Database()

def obtener_elementos(tabla, campo_nombre):
    """Obtiene los elementos de una tabla dada."""
    query = f"SELECT {campo_nombre} FROM natura_test.{tabla} ORDER BY {campo_nombre};"
    resultados = db.ejecutar_consulta(query, fetch=True)
    return [fila[0] for fila in resultados] if resultados else []

def actualizar_lista(listbox, elementos):
    """Actualiza la lista en la interfaz gráfica."""
    listbox.clear()
    listbox.addItems(elementos)

def abrir_abm(nombre_tabla, campo_nombre):
    ventana = QDialog()
    ventana.setWindowTitle(f"ABM {nombre_tabla}")
    ventana.resize(400, 600)

    layout = QVBoxLayout()
    label = QLabel(f"Nome {nombre_tabla}:")
    layout.addWidget(label)

    entry = QLineEdit()
    layout.addWidget(entry)

    listbox = QListWidget()
    layout.addWidget(listbox)

    # Cargar datos desde la BD
    elementos = obtener_elementos(nombre_tabla, campo_nombre)
    actualizar_lista(listbox, elementos)

    def agregar():
        elemento = entry.text().strip()
        if elemento:
            query = f'INSERT INTO natura_test.{nombre_tabla} ({campo_nombre}) VALUES (%s) ON CONFLICT DO NOTHING;'
            db.ejecutar_consulta(query, (elemento,))
            QMessageBox.information(ventana, "Successo", f"{nombre_tabla} '{elemento}' aggiunto correttamente.")
            entry.clear()
            actualizar_lista(listbox, obtener_elementos(nombre_tabla, campo_nombre))

    def eliminar():
        seleccion = listbox.currentItem()
        if seleccion:
            elemento = seleccion.text()
            query = f'DELETE FROM natura_test.{nombre_tabla} WHERE {campo_nombre} = %s;'
            db.ejecutar_consulta(query, (elemento,))
            QMessageBox.information(ventana, "Successo", f"{nombre_tabla} '{elemento}' rimosso con successo.")
            actualizar_lista(listbox, obtener_elementos(nombre_tabla, campo_nombre))

    def modificar():
        seleccion = listbox.currentItem()
        nuevo_elemento = entry.text().strip()
        if seleccion and nuevo_elemento:
            elemento = seleccion.text()
            query = f'UPDATE natura_test.{nombre_tabla} SET {campo_nombre} = %s WHERE {campo_nombre} = %s;'
            db.ejecutar_consulta(query, (nuevo_elemento, elemento))
            QMessageBox.information(ventana, "Successo", f"{nombre_tabla} '{elemento}' modificato in '{nuevo_elemento}'.")
            actualizar_lista(listbox, obtener_elementos(nombre_tabla, campo_nombre))

    botones = [
        QPushButton("Aggiungi", clicked=agregar),
        QPushButton("Modificare", clicked=modificar),
        QPushButton("Elimina", clicked=eliminar)
    ]
    for boton in botones:
        layout.addWidget(boton)

    ventana.setLayout(layout)
    ventana.exec()

def obtener_ortaggi_por_lavorazione(lavorazione_nome):
    """Obtiene los ortaggi asociados a una lavorazione específica."""
    query = '''
        SELECT o.ortaggio_nome 
        FROM natura_test.lavorazione_ortaggi lo
        JOIN natura_test.ortaggi o ON lo.ortaggio_key = o.ortaggio_key
        JOIN natura_test.lavorazioni l ON lo.lavorazione_key = l.lavorazione_key
        WHERE l.lavorazione_nome = %s;
    '''
    resultados = db.ejecutar_consulta(query, (lavorazione_nome,), fetch=True)
    return [fila[0] for fila in resultados] if resultados else []

def obtener_lavorazioni():
    """Obtiene todas las lavorazioni de la base de datos."""
    query = 'SELECT lavorazione_nome FROM natura_test.lavorazioni ORDER BY lavorazione_nome;'
    resultados = db.ejecutar_consulta(query, fetch=True)
    return [fila[0] for fila in resultados] if resultados else []

def obtener_ortaggi():
    """Obtiene todos los ortaggi de la base de datos."""
    query = 'SELECT ortaggio_nome FROM natura_test.ortaggi ORDER BY ortaggio_nome;'
    resultados = db.ejecutar_consulta(query, fetch=True)
    return [fila[0] for fila in resultados] if resultados else []

def actualizar_lista2(listbox):
    """Actualiza la lista de lavorazioni en la interfaz gráfica."""
    listbox.clear()
    listbox.addItems(obtener_lavorazioni())
def abrir_abm_lavorazione(): 
    ventana = QDialog()
    ventana.setWindowTitle("ABM Lavorazione")
    ventana.resize(600, 600)

    layout = QVBoxLayout()

    label = QLabel("Nome Lavorazione:")
    layout.addWidget(label)

    entry = QLineEdit()
    layout.addWidget(entry)

    listbox = QListWidget()
    layout.addWidget(listbox)
    actualizar_lista2(listbox)

    # Área de scroll para los ortaggi
    scroll_area = QScrollArea()
    scroll_widget = QWidget()
    grid_layout = QGridLayout()  # Usamos QGridLayout para organizar en una cuadrícula
    checkboxes = {}

    # Obtener ortaggi desde la base de datos
    ortaggi = obtener_ortaggi()
    if not ortaggi:
        grid_layout.addWidget(QLabel("⚠️ Nessun ortaggio trovato."), 0, 0)
    else:
        row, col = 0, 0
        for ortaggio in ortaggi:
            checkbox = QCheckBox(ortaggio)
            checkboxes[ortaggio] = checkbox
            grid_layout.addWidget(checkbox, row, col)

            # Pasar a la siguiente columna
            col += 1

            # Si hemos alcanzado el número máximo de columnas (por ejemplo, 4), pasamos a la siguiente fila
            if col > 3:
                col = 0
                row += 1

    scroll_widget.setLayout(grid_layout)

    # Ajustar tamaño para que los checkboxes sean visibles
    scroll_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    scroll_area.setWidget(scroll_widget)
    scroll_area.setWidgetResizable(True)
    scroll_area.setMinimumHeight(200)  # Asegurar que tenga altura suficiente

    layout.addWidget(scroll_area)

    def actualizar_checkboxes():
        """Actualiza los checkboxes según la lavorazione seleccionada."""
        seleccion = listbox.currentItem()
        if seleccion:
            nome_lavorazione = seleccion.text()
            ortaggi_seleccionados = obtener_ortaggi_por_lavorazione(nome_lavorazione)

            # Limpiar checkboxes antes de actualizar
            for checkbox in checkboxes.values():
                checkbox.setChecked(False)

            for ortaggio in ortaggi_seleccionados:
                if ortaggio in checkboxes:
                    checkboxes[ortaggio].setChecked(True)

    listbox.itemSelectionChanged.connect(actualizar_checkboxes)

    def agregar():
        """Agrega una nuova lavorazione y sus ortaggi asociados."""
        nome_lavorazione = entry.text().strip()
        if nome_lavorazione:
            query = 'INSERT INTO natura_test.lavorazioni (lavorazione_nome) VALUES (%s) ON CONFLICT DO NOTHING RETURNING lavorazione_key;'
            resultado = db.ejecutar_consulta(query, (nome_lavorazione,), fetch=True)
            
            if resultado:
                lavorazione_key = resultado[0][0]
                seleccionados = [ortaggio for ortaggio, cb in checkboxes.items() if cb.isChecked()]

                for ortaggio in seleccionados:
                    query = '''
                        INSERT INTO natura_test.lavorazione_ortaggi (lavorazione_key, ortaggio_key)
                        SELECT %s, ortaggio_key FROM natura_test.ortaggi WHERE ortaggio_nome = %s;
                    '''
                    db.ejecutar_consulta(query, (lavorazione_key, ortaggio))

                QMessageBox.information(ventana, "Successo", f"Lavorazione '{nome_lavorazione}' aggiunta con {seleccionados}.")
                entry.clear()
                actualizar_lista2(listbox)

    def eliminar():
        """Elimina la lavorazione seleccionada y su relación con ortaggi."""
        seleccion = listbox.currentItem()
        if seleccion:
            nome_lavorazione = seleccion.text()

            query = 'DELETE FROM natura_test.lavorazioni WHERE lavorazione_nome = %s;'
            db.ejecutar_consulta(query, (nome_lavorazione,))
            
            QMessageBox.information(ventana, "Successo", f"Lavorazione '{nome_lavorazione}' rimossa con successo.")
            actualizar_lista2(listbox)

    def modificar():
        """Modifica la lavorazione seleccionada y actualiza sus ortaggi relacionados."""
        seleccion = listbox.currentItem()
        nuovo_nome = entry.text().strip()  # Nuevo nombre ingresado
        
        if seleccion:
            nome_lavorazione = seleccion.text()  # Nombre actual en la base de datos

            # Verificar si se quiere cambiar el nombre o solo actualizar los ortaggi
            if nuovo_nome and nuovo_nome != nome_lavorazione:
                # Si hay un nuevo nombre, actualizarlo en la base de datos
                query = '''
                    UPDATE natura_test.lavorazioni
                    SET lavorazione_nome = %s
                    WHERE lavorazione_nome = %s
                    RETURNING lavorazione_key;
                '''
                resultado = db.ejecutar_consulta(query, (nuovo_nome, nome_lavorazione), fetch=True)
                if resultado:
                    lavorazione_key = resultado[0][0]
                    nome_finale = nuovo_nome  # Usar el nuevo nombre
            else:
                # Si no hay nuevo nombre, obtener la llave de la lavorazione actual
                query = '''
                    SELECT lavorazione_key FROM natura_test.lavorazioni WHERE lavorazione_nome = %s;
                '''
                resultado = db.ejecutar_consulta(query, (nome_lavorazione,), fetch=True)
                if resultado:
                    lavorazione_key = resultado[0][0]
                    nome_finale = nome_lavorazione  # Mantener el mismo nombre

            # Eliminar ortaggi asociados previamente
            query = 'DELETE FROM natura_test.lavorazione_ortaggi WHERE lavorazione_key = %s;'
            db.ejecutar_consulta(query, (lavorazione_key,))

            # Insertar nuevas relaciones con los ortaggi seleccionados
            seleccionados = [ortaggio for ortaggio, cb in checkboxes.items() if cb.isChecked()]
            for ortaggio in seleccionados:
                query = '''
                    INSERT INTO natura_test.lavorazione_ortaggi (lavorazione_key, ortaggio_key)
                    SELECT %s, ortaggio_key FROM natura_test.ortaggi WHERE ortaggio_nome = %s;
                '''
                db.ejecutar_consulta(query, (lavorazione_key, ortaggio))

            # Mostrar mensaje de éxito
            QMessageBox.information(ventana, "Successo", f"Lavorazione '{nome_lavorazione}' modificata.")

            # Actualizar la lista
            actualizar_lista2(listbox)

            # Volver a seleccionar el elemento actualizado en el listbox
            for i in range(listbox.count()):
                if listbox.item(i).text() == nome_finale:
                    listbox.setCurrentItem(listbox.item(i))
                    break
            
            # 🔹 ACTUALIZAR LOS CHECKBOXES MANUALMENTE
            ortaggi_actualizados = obtener_ortaggi_por_lavorazione(nome_finale)
            for ortaggio, checkbox in checkboxes.items():
                checkbox.setChecked(ortaggio in ortaggi_actualizados)

    botones = [
        QPushButton("Aggiungi", clicked=agregar),
        QPushButton("Modificare", clicked=modificar),
        QPushButton("Elimina", clicked=eliminar)
    ]

    for boton in botones:
        layout.addWidget(boton)

    ventana.setLayout(layout)
    ventana.exec()


# Funciones específicas para abrir cada ABM
def abrir_abm_ortaggi():
    abrir_abm("ortaggi", "ortaggio_nome")

def abrir_abm_imballaggi():
    abrir_abm("imballaggi", "imballaggio_nome")

def abrir_abm_pedane():
    abrir_abm("pedane", "pedana_nome")

def abrir_abm_clienti():
    abrir_abm("clienti", "cliente_nome")

def abrir_abm_magazzini():
    abrir_abm("magazzini", "magazzino_nome")

def abrir_abm_stati():
    abrir_abm("statiordine", "stato_nome")

def abm_lavorazione():
    abrir_abm_lavorazione()