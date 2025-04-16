from PySide6.QtWidgets import QMessageBox
from db import Database  # Importamos la conexión a la base de datos

db = Database()  # Creamos una instancia de la base de datos

def agregar_elemento(entry, list_widget, nombre_tabla, columna):
    """Agrega un elemento a la base de datos."""
    elemento = entry.text().strip()
    if elemento:
        query = f"INSERT INTO natura_test.{nombre_tabla} ({columna}) VALUES (%s) ON CONFLICT DO NOTHING;"
        db.ejecutar_consulta(query, (elemento,))
        QMessageBox.information(None, "Successo", f"'{elemento}' aggiunto correttamente.")
        entry.clear()
        actualizar_lista(list_widget, nombre_tabla, columna)

def actualizar_lista(list_widget, nombre_tabla, columna):
    """Carga los datos de la base de datos en el list_widget."""
    list_widget.clear()
    query = f"SELECT {columna} FROM natura_test.{nombre_tabla} ORDER BY {columna};"
    elementos = db.ejecutar_consulta(query, fetch=True)
    
    if elementos:
        for elemento in elementos:
            list_widget.addItem(elemento[0])  # Extrae el valor de la tupla

def eliminar_elemento(list_widget, nombre_tabla, columna):
    """Elimina un elemento seleccionado de la base de datos."""
    seleccion = list_widget.selectedItems()
    if seleccion:
        elemento = seleccion[0].text()
        query = f"DELETE FROM natura_test.{nombre_tabla} WHERE {columna} = %s;"
        db.ejecutar_consulta(query, (elemento,))
        QMessageBox.information(None, "Successo", f"'{elemento}' rimosso con successo.")
        actualizar_lista(list_widget, nombre_tabla, columna)

def modificar_elemento(entry, list_widget, nombre_tabla, columna):
    """Modifica un elemento en la base de datos."""
    seleccion = list_widget.selectedItems()
    if seleccion:
        elemento_actual = seleccion[0].text()
        nuevo_elemento = entry.text().strip()
        if nuevo_elemento:
            query = f"UPDATE natura_test.{nombre_tabla} SET {columna} = %s WHERE {columna} = %s;"
            db.ejecutar_consulta(query, (nuevo_elemento, elemento_actual))
            QMessageBox.information(None, "Successo", f"'{elemento_actual}' modificato in '{nuevo_elemento}'.")
            actualizar_lista(list_widget, nombre_tabla, columna)
