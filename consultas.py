from conexion import Conexion, pymysql
from clases import DatosUsuario, Producto
from validaciones import (
    validar_run, 
    validar_clave, 
    validar_producto
)

# Funciones de consultas SQL
# Funciones para usuarios
def obtener_datos_usuario(run, clave):
    try:
        # Validación de RUN y clave
        run = validar_run(run)
        if not run:
            return 1

        clave = validar_clave(clave)
        if not clave:
            return 2
        
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = ("SELECT u.run_usuario, u.clave_usuario, u.nombre_usuario, u.apellido_usuario, u.rol_FK, rol.rol_usuario, c.nombre_comuna, r.nombre_region "
                        "FROM USUARIOS AS u "
                        "INNER JOIN ROLES AS rol "
                            "ON u.rol_FK = rol.id_rol "
                        "INNER JOIN COMUNAS AS c "
                            "ON u.comuna_FK = c.id_comuna "
                        "INNER JOIN REGIONES AS r "
                            "ON c.region_FK = r.id_regiones "
                        "WHERE u.run_usuario = %s AND u.clave_usuario = %s")
            cursor.execute(sql_query, (run, clave))
            datos = cursor.fetchone()
        
        # Se guardan los datos
        if datos:
            run_user = datos[0].upper()
            clave_user = datos[1].upper()
            nombre_user = datos[2].upper()
            apellido_user = datos[3].upper()
            id_rol_usur = datos[4]
            rol_user = datos[5].upper()
            comuna_user = datos[6].upper()
            region_user = datos[7].upper()
            
            # Se crea una instancia con los datos
            user = DatosUsuario(run_user, nombre_user, apellido_user, comuna_user, region_user, rol_user, clave_user, id_rol_usur)
            return user

        return 3  # No se encontraron datos para el usuario especificado.
    
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return 4  # Ocurrió un error en la operación de la base de datos.
    
    except Exception as error:
        print(f"Error desconocido: {error}")
        return 4  # Ocurrió un error en la operación de la base de datos.

# Funciones para productos
def buscar_producto(dato_producto):
    try:
        # Normalizo los datos
        # Validación de RUN y clave
        dato_producto = validar_producto(dato_producto)
        if not dato_producto:
            return False
        
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = ("SELECT codigo_producto, nombre_producto "
                         "FROM PRODUCTOS " 
                         "WHERE codigo_producto = %s OR nombre_producto LIKE %s")
            cursor.execute(sql_query, (dato_producto, f"%{dato_producto}%"))
            resultados = cursor.fetchall()
            
            # Verificar si se encontraron resultados
            cantidad_productos = len(resultados)
            if cantidad_productos > 0:
                return cantidad_productos

        return False  # No se encontró el producto.
    
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.

def obtener_datos_producto(dato_producto):
    try:
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = ("SELECT p.codigo_producto, p.nombre_producto, p.precio_producto, m.nombre_marca, c.nombre_categoria "
                        "FROM PRODUCTOS AS p "
                        "INNER JOIN MARCAS AS m "
                            "ON p.marca_FK = m.id_marca "
                        "INNER JOIN CATEGORIAS AS c "
                            "ON p.categoria_FK = c.id_categoria "
                        "WHERE codigo_producto = %s OR nombre_producto LIKE %s")
            cursor.execute(sql_query, (dato_producto, f"%{dato_producto}%"))
            datos = cursor.fetchone()
        
        # Se guardan los datos
        if datos:
            codigo_producto = datos[0].upper()
            nombre_producto = datos[1].upper()
            precio_producto = datos[2]
            marca = datos[3].upper()
            categoria = datos[4].upper()
            
            # Se crea una instancia con los datos
            producto = Producto(codigo_producto, nombre_producto, precio_producto, marca, categoria)
            return producto

        return None  # No se encontraron datos para el usuario especificado.
    
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.

def obtener_lista_productos(dato_producto):
    try:
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = ("SELECT codigo_producto, nombre_producto "
                         "FROM PRODUCTOS " 
                         "WHERE codigo_producto = %s OR nombre_producto LIKE %s")
            cursor.execute(sql_query, (dato_producto, f"%{dato_producto}%"))
            datos = cursor.fetchall()
        
        # Se guardan los datos en una lista de diccionarios
        productos = []
        for dato in datos:
            codigo_producto = dato[0].upper()
            nombre_producto = dato[1].upper()
            producto = {"codigo": codigo_producto, "nombre": nombre_producto}
            productos.append(producto)
        
        return productos
    
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None
    
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None

