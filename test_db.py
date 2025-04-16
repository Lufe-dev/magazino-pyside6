from db import conectar

conexion = conectar()

if conexion:
    print("Se estableció la conexión correctamente.")
    conexion.close()  # Cierra la conexión después de la prueba
else:
    print("No se pudo conectar a la base de datos.")
