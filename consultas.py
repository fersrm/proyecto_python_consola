from conexion import Conexion, pymysql
from clases import DatosUsuario, Producto, DatosCliente
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
            sql_query = (
                "SELECT u.id_usuario, u.run_usuario, u.clave_usuario, u.nombre_usuario, u.apellido_usuario, u.rol_FK, rol.rol_usuario, c.nombre_comuna, r.nombre_region "
                "FROM USUARIOS AS u "
                "INNER JOIN ROLES AS rol "
                    "ON u.rol_FK = rol.id_rol "
                "INNER JOIN COMUNAS AS c "
                    "ON u.comuna_FK = c.id_comuna "
                "INNER JOIN REGIONES AS r "
                    "ON c.region_FK = r.id_regiones "
                "WHERE u.run_usuario = %s AND u.clave_usuario = %s"
            )
            cursor.execute(sql_query, (run, clave))
            datos = cursor.fetchone()
        
        # Se guardan los datos
        if datos:
            id_user, run_user, clave_user, nombre_user, apellido_user, id_rol_usur, rol_user, comuna_user, region_user = datos
            
            # Se crea una instancia con los datos
            user = DatosUsuario(id_user, run_user, nombre_user, apellido_user, comuna_user, region_user, rol_user, clave_user, id_rol_usur)
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
        # Validación de nombre o código de producto
        dato_producto = validar_producto(dato_producto)
        if not dato_producto:
            return False
        
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = (
                "SELECT codigo_producto, nombre_producto "
                "FROM PRODUCTOS " 
                "WHERE codigo_producto = %s OR nombre_producto LIKE %s"
            )
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
            sql_query = (
                "SELECT p.id_producto, p.codigo_producto, p.nombre_producto, p.precio_producto, m.nombre_marca, c.nombre_categoria "
                "FROM PRODUCTOS AS p "
                "INNER JOIN MARCAS AS m "
                    "ON p.marca_FK = m.id_marca "
                "INNER JOIN CATEGORIAS AS c "
                    "ON p.categoria_FK = c.id_categoria "
                "WHERE codigo_producto = %s OR nombre_producto LIKE %s"
            )
            cursor.execute(sql_query, (dato_producto, f"%{dato_producto}%"))
            datos = cursor.fetchone()
        
        # Se guardan los datos   
        if datos:
            id_producto, codigo_producto, nombre_producto, precio_producto, marca, categoria = datos
            
            # Se crea una instancia con los datos
            producto = Producto(id_producto, codigo_producto, nombre_producto, precio_producto, marca, categoria)
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
            sql_query = (
                "SELECT codigo_producto, nombre_producto, precio_producto  "
                "FROM PRODUCTOS " 
                "WHERE codigo_producto = %s OR nombre_producto LIKE %s"
            )
            cursor.execute(sql_query, (dato_producto, f"%{dato_producto}%"))
            datos = cursor.fetchall()
        
        # Se guardan los datos en una lista de diccionarios
        productos = []
        for dato in datos:
            codigo_producto = dato[0].upper()
            nombre_producto = dato[1].upper()
            precio_producto = dato[2]
            producto = {"codigo": codigo_producto, "nombre": nombre_producto, "precio": precio_producto}
            productos.append(producto)
        
        return productos
    
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None
    
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None

# Fucion pasar cargar detalle carrito a BBDD y generar boleta o factura
def generar_venta(carrito, id_cliente, id_vendedor, tipo_venta):
    if not carrito:
        return False  # Carrito vacío, no se puede generar la venta

    try:
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_create = "CREATE TEMPORARY TABLE IF NOT EXISTS detalle_temp (id_producto INTEGER, cantidad INTEGER, total_producto INTEGER)"
            # Crea una tabla temporal en la base de datos
            cursor.execute(sql_create)

            for item in carrito:
                producto = item['producto']
                cantidad = item['cantidad']
                precio_unitario = producto.get_precio()
                total = cantidad * precio_unitario

                sql_query = "INSERT INTO detalle_temp (id_producto, cantidad, total_producto) VALUES (%s, %s, %s)"
                # Inserta los datos en la tabla temporal
                cursor.execute(sql_query, (producto.get_id(),cantidad,total))

           
            # Llama al procedimiento almacenado
            cursor.execute("CALL generar_venta(%s, %s, %s)", (id_cliente, id_vendedor, tipo_venta))
            return True  # Proceso almacenado ejecutado correctamente

    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.

    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.

# Funcion para clientes
def obtener_datos_Cliente(run):
    try:
        # Validación de RUN y clave
        run = validar_run(run)
        if not run:
            return 1
        
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = (
                "SELECT cl.id_cliente, cl.run_cliente, cl.nombre_cliente, cl.apellido_cliente, e.razon_social, t.nombre_giro, cl.direccion, c.nombre_comuna, r.nombre_region "
                "FROM CLIENTES AS cl "
                "INNER JOIN RAZON_SOCIAL AS e "
                    "ON cl.razon_social_FK = e.id_razon_social "
                "INNER JOIN TIPO_GIRO AS t "
                    "ON cl.tipo_giro_FK = t.id_giro "
                "INNER JOIN COMUNAS AS c "
                    "ON cl.comuna_FK = c.id_comuna "
                "INNER JOIN REGIONES AS r "
                    "ON c.region_FK = r.id_regiones "
                "WHERE cl.run_cliente = %s "
            )
            cursor.execute(sql_query, (run))
            datos = cursor.fetchone()
    
        # Se guardan los datos
        if datos:
            id_cliente, run_cliente, nombre_cliente, apellido_cliente, razon_social, tipo_giro, direccion_cliente, comuna_cliente, region_cliente = datos
            
            # Se crea una instancia con los datos
            cliente = DatosCliente(id_cliente, run_cliente, nombre_cliente, apellido_cliente, comuna_cliente, region_cliente, razon_social, direccion_cliente, tipo_giro)
            return cliente

        return 2  # No se encontraron datos para el usuario especificado.
    
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return 3  # Ocurrió un error en la operación de la base de datos.
    
    except Exception as error:
        print(f"Error desconocido: {error}")
        return 3  # Ocurrió un error en la operación de la base de datos.
