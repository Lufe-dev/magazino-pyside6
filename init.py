import tkinter as tk
from tkinter import messagebox

# Listas globales para almacenar los elementos
verduras = []
cajas = []
pallets = []
proveedores = []
estados_pedido = []
linea_produccion = []

# Función para agregar un elemento a la lista
def agregar_elemento(entry_elemento, ventana_elementos, lista_elementos, nombre_elemento):
    elemento = entry_elemento.get()
    if elemento:
        lista_elementos.append(elemento)
        messagebox.showinfo("Éxito", f"{nombre_elemento} '{elemento}' agregada correctamente.")
        entry_elemento.delete(0, tk.END)  # Limpiar el campo de texto
        actualizar_lista(ventana_elementos, lista_elementos)
    else:
        messagebox.showwarning("Advertencia", f"Por favor ingrese el nombre de la {nombre_elemento.lower()}.")

# Función para actualizar la lista de elementos
def actualizar_lista(ventana_elementos, lista_elementos):
    listbox_elementos.delete(0, tk.END)
    for elemento in lista_elementos:
        listbox_elementos.insert(tk.END, elemento)

# Función para eliminar un elemento seleccionado
def eliminar_elemento(ventana_elementos, lista_elementos, nombre_elemento):
    seleccion = listbox_elementos.curselection()
    if seleccion:
        elemento = listbox_elementos.get(seleccion)
        lista_elementos.remove(elemento)
        messagebox.showinfo("Éxito", f"{nombre_elemento} '{elemento}' eliminada correctamente.")
        actualizar_lista(ventana_elementos, lista_elementos)
    else:
        messagebox.showwarning("Advertencia", f"Por favor seleccione una {nombre_elemento.lower()} para eliminar.")

# Función para modificar un elemento seleccionado
def modificar_elemento(entry_elemento, ventana_elementos, lista_elementos, nombre_elemento):
    seleccion = listbox_elementos.curselection()
    if seleccion:
        elemento_seleccionado = listbox_elementos.get(seleccion)
        nuevo_elemento = entry_elemento.get()
        if nuevo_elemento:
            index = lista_elementos.index(elemento_seleccionado)
            lista_elementos[index] = nuevo_elemento
            messagebox.showinfo("Éxito", f"{nombre_elemento} '{elemento_seleccionado}' modificada a '{nuevo_elemento}'.")
            entry_elemento.delete(0, tk.END)
            actualizar_lista(ventana_elementos, lista_elementos)
        else:
            messagebox.showwarning("Advertencia", f"Por favor ingrese un nuevo nombre para la {nombre_elemento.lower()}.")
    else:
        messagebox.showwarning("Advertencia", f"Por favor seleccione una {nombre_elemento.lower()} para modificar.")

# Función para mostrar la pantalla ABM de Verduras
def abrir_abm_verduras():
    ventana_verduras = tk.Toplevel()  # Crea una ventana secundaria
    ventana_verduras.title("ABM Verduras")

    # Crear una etiqueta y un campo de entrada para agregar una verdura
    label_verdura = tk.Label(ventana_verduras, text="Nombre de la Verdura:")
    label_verdura.pack(padx=10, pady=10)
    entry_verdura = tk.Entry(ventana_verduras)
    entry_verdura.pack(padx=10, pady=10)

    # Crear botones para las acciones
    boton_agregar = tk.Button(ventana_verduras, text="Agregar Verdura", command=lambda: agregar_elemento(entry_verdura, ventana_verduras, verduras, "Verdura"))
    boton_agregar.pack(padx=10, pady=10)
    
    boton_modificar = tk.Button(ventana_verduras, text="Modificar Verdura", command=lambda: modificar_elemento(entry_verdura, ventana_verduras, verduras, "Verdura"))
    boton_modificar.pack(padx=10, pady=10)

    boton_eliminar = tk.Button(ventana_verduras, text="Eliminar Verdura", command=lambda: eliminar_elemento(ventana_verduras, verduras, "Verdura"))
    boton_eliminar.pack(padx=10, pady=10)

    # Crear un Listbox para mostrar las verduras
    global listbox_elementos
    listbox_elementos = tk.Listbox(ventana_verduras, selectmode=tk.SINGLE)
    listbox_elementos.pack(padx=10, pady=10)

    # Actualizar la lista de verduras
    actualizar_lista(ventana_verduras, verduras)

    # Mostrar la ventana
    ventana_verduras.mainloop()

# Función para mostrar la pantalla ABM de Cajas
def abrir_abm_cajas():
    ventana_cajas = tk.Toplevel()  # Crea una ventana secundaria
    ventana_cajas.title("ABM Cajas")

    # Crear una etiqueta y un campo de entrada para agregar una caja
    label_caja = tk.Label(ventana_cajas, text="Nombre de la Caja:")
    label_caja.pack(padx=10, pady=10)
    entry_caja = tk.Entry(ventana_cajas)
    entry_caja.pack(padx=10, pady=10)

    # Crear botones para las acciones
    boton_agregar = tk.Button(ventana_cajas, text="Agregar Caja", command=lambda: agregar_elemento(entry_caja, ventana_cajas, cajas, "Caja"))
    boton_agregar.pack(padx=10, pady=10)
    
    boton_modificar = tk.Button(ventana_cajas, text="Modificar Caja", command=lambda: modificar_elemento(entry_caja, ventana_cajas, cajas, "Caja"))
    boton_modificar.pack(padx=10, pady=10)

    boton_eliminar = tk.Button(ventana_cajas, text="Eliminar Caja", command=lambda: eliminar_elemento(ventana_cajas, cajas, "Caja"))
    boton_eliminar.pack(padx=10, pady=10)

    # Crear un Listbox para mostrar las cajas
    global listbox_elementos
    listbox_elementos = tk.Listbox(ventana_cajas, selectmode=tk.SINGLE)
    listbox_elementos.pack(padx=10, pady=10)

    # Actualizar la lista de cajas
    actualizar_lista(ventana_cajas, cajas)

    # Mostrar la ventana
    ventana_cajas.mainloop()

# Función para mostrar la pantalla ABM de Pallets
def abrir_abm_pallets():
    ventana_pallets = tk.Toplevel()  # Crea una ventana secundaria
    ventana_pallets.title("ABM Pallets")

    # Crear una etiqueta y un campo de entrada para agregar un pallet
    label_pallet = tk.Label(ventana_pallets, text="Nombre del Pallet:")
    label_pallet.pack(padx=10, pady=10)
    entry_pallet = tk.Entry(ventana_pallets)
    entry_pallet.pack(padx=10, pady=10)

    # Crear botones para las acciones
    boton_agregar = tk.Button(ventana_pallets, text="Agregar Pallet", command=lambda: agregar_elemento(entry_pallet, ventana_pallets, pallets, "Pallet"))
    boton_agregar.pack(padx=10, pady=10)
    
    boton_modificar = tk.Button(ventana_pallets, text="Modificar Pallet", command=lambda: modificar_elemento(entry_pallet, ventana_pallets, pallets, "Pallet"))
    boton_modificar.pack(padx=10, pady=10)

    boton_eliminar = tk.Button(ventana_pallets, text="Eliminar Pallet", command=lambda: eliminar_elemento(ventana_pallets, pallets, "Pallet"))
    boton_eliminar.pack(padx=10, pady=10)

    # Crear un Listbox para mostrar los pallets
    global listbox_elementos
    listbox_elementos = tk.Listbox(ventana_pallets, selectmode=tk.SINGLE)
    listbox_elementos.pack(padx=10, pady=10)

    # Actualizar la lista de pallets
    actualizar_lista(ventana_pallets, pallets)

    # Mostrar la ventana
    ventana_pallets.mainloop()

# Función para mostrar la pantalla ABM de Proveedores
def abrir_abm_proveedores():
    ventana_proveedores = tk.Toplevel()  # Crea una ventana secundaria
    ventana_proveedores.title("ABM Proveedores")

    # Crear una etiqueta y un campo de entrada para agregar un proveedor
    label_proveedor = tk.Label(ventana_proveedores, text="Nombre del Proveedor:")
    label_proveedor.pack(padx=10, pady=10)
    entry_proveedor = tk.Entry(ventana_proveedores)
    entry_proveedor.pack(padx=10, pady=10)

    # Crear botones para las acciones
    boton_agregar = tk.Button(ventana_proveedores, text="Agregar Proveedor", command=lambda: agregar_elemento(entry_proveedor, ventana_proveedores, proveedores, "Proveedor"))
    boton_agregar.pack(padx=10, pady=10)
    
    boton_modificar = tk.Button(ventana_proveedores, text="Modificar Proveedor", command=lambda: modificar_elemento(entry_proveedor, ventana_proveedores, proveedores, "Proveedor"))
    boton_modificar.pack(padx=10, pady=10)

    boton_eliminar = tk.Button(ventana_proveedores, text="Eliminar Proveedor", command=lambda: eliminar_elemento(ventana_proveedores, proveedores, "Proveedor"))
    boton_eliminar.pack(padx=10, pady=10)

    # Crear un Listbox para mostrar los proveedores
    global listbox_elementos
    listbox_elementos = tk.Listbox(ventana_proveedores, selectmode=tk.SINGLE)
    listbox_elementos.pack(padx=10, pady=10)

    # Actualizar la lista de proveedores
    actualizar_lista(ventana_proveedores, proveedores)

    # Mostrar la ventana
    ventana_proveedores.mainloop()

# Función para mostrar la pantalla ABM de Estados de Pedido
def abrir_abm_estados():
    ventana_estados = tk.Toplevel()  # Crea una ventana secundaria
    ventana_estados.title("ABM Estados de Pedido")

    # Crear una etiqueta y un campo de entrada para agregar un estado
    label_estado = tk.Label(ventana_estados, text="Nombre del Estado:")
    label_estado.pack(padx=10, pady=10)
    entry_estado = tk.Entry(ventana_estados)
    entry_estado.pack(padx=10, pady=10)

    # Crear botones para las acciones
    boton_agregar = tk.Button(ventana_estados, text="Agregar Estado", command=lambda: agregar_elemento(entry_estado, ventana_estados, estados_pedido, "Estado"))
    boton_agregar.pack(padx=10, pady=10)
    
    boton_modificar = tk.Button(ventana_estados, text="Modificar Estado", command=lambda: modificar_elemento(entry_estado, ventana_estados, estados_pedido, "Estado"))
    boton_modificar.pack(padx=10, pady=10)

    boton_eliminar = tk.Button(ventana_estados, text="Eliminar Estado", command=lambda: eliminar_elemento(ventana_estados, estados_pedido, "Estado"))
    boton_eliminar.pack(padx=10, pady=10)

    # Crear un Listbox para mostrar los estados
    global listbox_elementos
    listbox_elementos = tk.Listbox(ventana_estados, selectmode=tk.SINGLE)
    listbox_elementos.pack(padx=10, pady=10)

    # Actualizar la lista de estados
    actualizar_lista(ventana_estados, estados_pedido)

    # Mostrar la ventana
    ventana_estados.mainloop()

# Función para ver la línea de producción
def ver_linea_produccion():
    ventana_produccion = tk.Toplevel()
    ventana_produccion.title("Línea de Producción")
    label_produccion = tk.Label(ventana_produccion, text="Estado actual de la línea de producción:")
    label_produccion.pack(padx=10, pady=10)

    lista_produccion = "\n".join(linea_produccion) if linea_produccion else "No hay productos en la línea de producción."
    label_linea = tk.Label(ventana_produccion, text=lista_produccion)
    label_linea.pack(padx=10, pady=10)

    ventana_produccion.mainloop()

# Función para agregar a la línea de producción
def agregar_a_linea_produccion():
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar a Línea de Producción")

    # Crear un campo para seleccionar los elementos
    label_verdura = tk.Label(ventana_agregar, text="Selecciona una Verdura:")
    label_verdura.pack(padx=10, pady=10)
    combobox_verdura = tk.OptionMenu(ventana_agregar, verduras)
    combobox_verdura.pack(padx=10, pady=10)

    # Puedes añadir más campos para otros elementos (cajas, pallets, proveedores)

    # Botón para agregar a la línea de producción
    boton_agregar_linea = tk.Button(ventana_agregar, text="Agregar a Línea", command=lambda: linea_produccion.append("Verdura seleccionada"))
    boton_agregar_linea.pack(padx=10, pady=10)

    ventana_agregar.mainloop()

# Función principal
def main():
    ventana = tk.Tk()
    ventana.title("Gestión de Producción de Verduras")

    # Menú principal
    menu = tk.Menu(ventana)
    ventana.config(menu=menu)

    # Submenú de ABM
    menu_abm = tk.Menu(menu)
    menu.add_cascade(label="ABM", menu=menu_abm)
    menu_abm.add_command(label="Verduras", command=abrir_abm_verduras)
    menu_abm.add_command(label="Cajas", command=abrir_abm_cajas)
    menu_abm.add_command(label="Pallets", command=abrir_abm_pallets)
    menu_abm.add_command(label="Proveedores", command=abrir_abm_proveedores)
    menu_abm.add_command(label="Estados de Pedido", command=abrir_abm_estados)

    # Submenú de Producción
    menu_produccion = tk.Menu(menu)
    menu.add_cascade(label="Producción", menu=menu_produccion)
    menu_produccion.add_command(label="Ver Línea de Producción", command=ver_linea_produccion)
    menu_produccion.add_command(label="Agregar a Línea de Producción", command=agregar_a_linea_produccion)

    ventana.mainloop()

if __name__ == "__main__":
    main()
