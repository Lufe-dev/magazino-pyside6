import psycopg2
import atexit  # Permite ejecutar código al salir del programa

class Database:
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.conn = None
        self.conectar()
        atexit.register(self.cerrar_conexion)  # Se ejecuta al salir del programa

    def conectar(self):
        """Intenta conectar a la base de datos y guarda la conexión en self.conn."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    dbname='Natura_test',
                    user='postgres',
                    password='test',
                    host='localhost',
                    port='5432'
                )
                print("✅ Conexión establecida con PostgreSQL")
            except Exception as e:
                print(f"❌ Error al conectar a la base de datos: {e}")
                self.conn = None

    def ejecutar_consulta(self, query, params=None, fetch=False, como_diccionario=False):
        """Ejecuta una consulta SQL. Si es SELECT, devuelve los resultados en el formato solicitado (tuplas o diccionarios)."""
        if self.conn is None:
            print("⚠️ No hay conexión activa. Intentando reconectar...")
            self.conectar()

        if self.conn:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, params)
                    if fetch:
                        if como_diccionario:
                            # Obtener los nombres de las columnas
                            columnas = [desc[0] for desc in cursor.description]
                            rows = cursor.fetchall()
                            # Convertir las filas en diccionarios
                            result = [dict(zip(columnas, row)) for row in rows]
                            return result
                        else:
                            return cursor.fetchall()  # Devuelve como tupla
                    self.conn.commit()
            except Exception as e:
                self.conn.rollback()  # Deshacer cambios en caso de error
                print(f"❌ Error en la consulta: {e}")
                self.reiniciar_conexion()
                return [] if fetch else None  # Evita devolver None en una consulta SELECT


    def reiniciar_conexion(self):
        """Cierra la conexión y la intenta restablecer."""
        self.cerrar_conexion()
        self.conectar()

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("🔌 Conexión cerrada.")
            self.conn = None
