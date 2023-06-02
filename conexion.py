import pymysql

# Clase de la conexion a Base de datos
class Conexion:
    def __init__(self):
        try:
            self.conexion = None
            self.cursor = None
        except pymysql.Error as e:
            print("Error al conectar a la base de datos:", e)

    def __enter__(self):
        # Establecer la conexión con la base de datos
        self.conexion = pymysql.connect(
            host = "localhost",
            database = "bazar",
            user = "root",
            password = ""
        )
        self.cursor = self.conexion.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            # Cerrar el cursor y la conexión al finalizar
            if self.cursor:
                self.cursor.close()
            if self.conexion:
                self.conexion.close()
        except pymysql.Error as e:
            print("Error al cerrar la conexión:", e)

    def get_cursor(self):
        return self.cursor
