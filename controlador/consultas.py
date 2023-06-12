from conexion.conexion import Conexion, pymysql
from controlador.modelo.clases import (
    DatosUsuario, 
    Producto, 
    DatosCliente, 
    DetalleVentas, 
    DetalleEmpresa,
    Ventas
)
from controlador.validaciones import (
    validar_run, 
    validar_clave, 
    validar_producto
)

# Funciones de consultas SQL
# Funciones para usuarios
def obtener_datos_usuario(run, clave=None, rol=None):
    try:
        # Validación de RUN y clave
        run = validar_run(run)
        if not run:
            return 1
        if clave is not None:
            clave = validar_clave(clave)
            if not clave:
                return 2
        # Construir la consulta SQL
        sql_query = (
            "SELECT u.id_usuario, u.run_usuario, u.clave_usuario, u.nombre_usuario, u.apellido_usuario, u.rol_FK, rol.rol_usuario, c.nombre_comuna, r.nombre_region "
            "FROM USUARIOS AS u "
            "INNER JOIN ROLES AS rol "
            "ON u.rol_FK = rol.id_rol "
            "INNER JOIN COMUNAS AS c "
            "ON u.comuna_FK = c.id_comuna "
            "INNER JOIN REGIONES AS r "
            "ON c.region_FK = r.id_regiones "
            "WHERE u.run_usuario = %s"
        )

        params = [run]
        # Si viene la clave la agrega a la consulta
        if clave is not None:
            sql_query += " AND u.clave_usuario = %s"
            params.append(clave)
        # Si viene el rol lo agrega a la consulta
        if rol is not None:
            sql_query += " AND u.rol_FK = %s"
            params.append(rol)
        # Ejecutar la consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            cursor.execute(sql_query, params)
            datos = cursor.fetchone()
        # Verificar si se obtuvieron resultados
        if not datos:
            return 3  # No se encontraron datos para el usuario especificado.
        # Se guardan los datos
        id_user, run_user, clave_user, nombre_user, apellido_user, id_rol_usur, rol_user, comuna_user, region_user = datos
        # Se crea una instancia con los datos
        user = DatosUsuario(id_user, run_user, nombre_user, apellido_user, comuna_user, region_user, rol_user, clave_user, id_rol_usur)
        return user
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error desconocido.

# Funciones para productos
def buscar_producto(dato_producto):
    try:
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
            # Verificar si se obtuvieron resultados
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
                "WHERE p.codigo_producto = %s OR nombre_producto LIKE %s"
            )
            cursor.execute(sql_query, (dato_producto, f"%{dato_producto}%"))
            datos = cursor.fetchone()
        # Verificar si se obtuvieron resultados    
        if not datos:
            return None  # No se encontraron datos para el usuario especificado.
        # Se guardan los datos   
        id_producto, codigo_producto, nombre_producto, precio_producto, marca, categoria = datos
        # Se crea una instancia con los datos
        producto = Producto(id_producto, codigo_producto, nombre_producto, precio_producto, marca, categoria)
        return producto
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
        # Verificar si se obtuvieron resultados
        if not datos:
            return None    
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
            cursor.callproc("generar_venta", (id_cliente, id_vendedor, tipo_venta))
            # Obtener el primer conjunto de resultados (id_compra, total_venta)
            datos_compra = cursor.fetchone()
            # Avanzar al siguiente conjunto de resultados
            cursor.nextset()   
            # Obtener el segundo conjunto de resultados (cantidad_productos, total_productos, codigo_producto, nombre_producto, precio_unitario)
            detalle_compra = cursor.fetchall()
            # Desempaquetar los datos de venta
            id_compra, total_compra, fecha_venta = datos_compra
            # Extraer los datos del detalle de compra
            cantidad_productos = []
            total_productos = []
            codigo_productos = []
            nombre_productos = []
            precio_unitarios = []
            for fila in detalle_compra:
                cantidad_productos.append(fila[0])
                total_productos.append(fila[1])
                codigo_productos.append(fila[2])
                nombre_productos.append(fila[3])
                precio_unitarios.append(fila[4])
            # Crear una instancia de DetalleVentas con los datos
            detalle_venta = DetalleVentas(
                cantidad_productos,
                total_productos,
                id_compra,
                total_compra,
                codigo_productos,
                nombre_productos,
                precio_unitarios,
                fecha_venta
            )
            return detalle_venta

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
        # Verificar si se obtuvieron resultados
        if not datos:
            return 2  # No se encontraron datos para el usuario especificado.
        # Se guardan los datos
        id_cliente, run_cliente, nombre_cliente, apellido_cliente, razon_social, tipo_giro, direccion_cliente, comuna_cliente, region_cliente = datos
        # Se crea una instancia con los datos
        cliente = DatosCliente(
            id_cliente, 
            run_cliente, 
            nombre_cliente, 
            apellido_cliente, 
            comuna_cliente, 
            region_cliente, 
            razon_social, 
            direccion_cliente, 
            tipo_giro
        )
        return cliente
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return 3  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return 3  # Ocurrió un error en la operación de la base de datos.

# Funcion Registrar cliente
def tablas_registrar_cliente():
    try:
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            # Llama al procedimiento almacenado
            cursor.callproc("traer_tablas_cliente", ())
            # Obtener el primer conjunto de resultados (Tipo de giro)
            datos_tipo_giro = cursor.fetchall()
            # Avanzar al siguiente conjunto de resultados
            cursor.nextset()   
            # Obtener el segundo conjunto de resultados (razon social)
            datos_razon_social = cursor.fetchall()
            # Avanzar al siguiente conjunto de resultados
            cursor.nextset()   
            # Obtener el tercer conjunto de resultados (Tipo de giro)
            datos_comunas = cursor.fetchall()
        # Desempaquetar los datos de venta
        tipo_giro = []
        for fila in datos_tipo_giro:
            tipo_giro.append(fila)
        razon_social = []
        for fila in datos_razon_social:
            razon_social.append(fila)
        comunas = []
        for fila in datos_comunas:
            comunas.append(fila)
        return tipo_giro, razon_social , comunas
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    
def insertar_cliente(datos_cliente, id_vendedor):
    try:
        # Desempaquetar los datos
        run_cliente, nombre, apellido, direccion, tipo_giro, razon_social, comuna = datos_cliente
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            # Llama al procedimiento almacenado utilizando execute
            cursor.callproc("registro_cliente",(run_cliente, nombre, apellido, direccion, tipo_giro, razon_social, comuna ,id_vendedor))
            # Obtener los resultados del procedimiento almacenado
            datos = cursor.fetchone()
            # Verificar si se obtuvieron resultados
        if not datos:
            return None
        # Obtener los datos del cliente
        id_cliente, run_cliente, nombre_cliente, apellido_cliente, razon_social, tipo_giro, direccion_cliente, comuna_cliente, region_cliente = datos
        # Se crea una instancia con los datos
        nuevo_cliente = DatosCliente(
            id_cliente, 
            run_cliente, 
            nombre_cliente, 
            apellido_cliente, 
            comuna_cliente, 
            region_cliente, 
            razon_social, 
            direccion_cliente, 
            tipo_giro
        )
        return nuevo_cliente
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error desconocido en la operación de la base de datos.

# Funcion para obtener datos generales de la empresa
def obtener_datos_empresa():
    try:
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = (
                "SELECT id_datos_empresa, nombre_empresa, rut_empresa, direccion_empresa, estado , IVA "
                "FROM datos_empresa WHERE id_datos_empresa = 1 "
            )
            cursor.execute(sql_query)
            datos = cursor.fetchone()
        # Verificar si se obtuvieron resultados    
        if not datos:
            return None  # No se encontraron datos.
        # Se guardan los datos   
        id_local, nombre_local, rut_local, direccion_local, estado , IVA = datos
        # Se crea una instancia con los datos
        datos_local = DetalleEmpresa(id_local, nombre_local, rut_local, direccion_local, IVA, estado)
        return datos_local
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    
#----------------------------------------------------------------------------------------
# Consultas para el jefe de ventas
#----------------------------------------------------------------------------------------
# Funciones para registrar un nuevo producto
def tablas_registrar_producto():
    try:
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            # Llama al procedimiento almacenado
            cursor.callproc("traer_tablas_producto", ())
            # Obtener el primer conjunto de resultados (Marcas)
            datos_marcas = cursor.fetchall()
            # Avanzar al siguiente conjunto de resultados
            cursor.nextset()   
            # Obtener el segundo conjunto de resultados (Categorias)
            datos_categorias = cursor.fetchall()
        # Desempaquetar los datos 
        marcas = []
        for fila in datos_marcas:
            marcas.append(fila)
        categorias = []
        for fila in datos_categorias:
            categorias.append(fila)
        return marcas, categorias
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.

def insetar_producto(datos_nuevo_producto, id_usuario):
    try:
        # Desempaquetar los datos
        codigo_producto,nombre_producto, precio, marca, categoria = datos_nuevo_producto
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            # Llama al procedimiento almacenado utilizando execute
            cursor.callproc("registro_producto",(codigo_producto, nombre_producto, precio, marca, categoria, id_usuario))
            # Obtener los resultados del procedimiento almacenado
            datos = cursor.fetchone()
            # Verificar si se obtuvieron resultados
        if not datos:
            return None
        # Se guardan los datos   
        id_producto, codigo_producto, nombre_producto, precio_producto, marca, categoria = datos
        # Se crea una instancia con los datos
        producto = Producto(id_producto, codigo_producto, nombre_producto, precio_producto, marca, categoria)
        return producto
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None  # Ocurrió un error desconocido en la operación de la base de datos.

# Funcionabilidad para generar informes
def generar_informe(opcion, condicion_busqueda):
    if opcion == 1:
        fecha_busqueda = f"{condicion_busqueda}%"
        where = f"WHERE v.fecha_emcion LIKE '{fecha_busqueda}'"
    else:
        where = f"WHERE v.usuario_FK = (SELECT id_usuario FROM USUARIOS WHERE run_usuario =  '{condicion_busqueda.get_run()}')"
        print(where)
    # utilizar en la consulta
    try:
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = (
                "SELECT v.id_venta, date(v.fecha_emcion) AS fecha, f.total_factura AS monto_factura, b.total_boleta AS monto_boleta "
                "FROM VENTAS v "
                "LEFT JOIN FACTURAS f ON v.id_venta = f.venta_FK "
                "LEFT JOIN BOLETAS b ON v.id_venta = b.venta_FK "
                f"{where}"
            )
            cursor.execute(sql_query)
            resultados = cursor.fetchall()
        # Verificar si se obtuvieron resultados
        if not resultados :
            return False
        # Extraer los datos
        id_venta = []
        fecha = []
        total_factura = []
        total_boleta = []
        for fila in resultados:
            id_venta.append(fila[0])
            fecha.append(fila[1])
            total_factura.append(fila[2])
            total_boleta.append(fila[3])
        total_venta = [total_factura, total_boleta]
        # Crear una instancia
        ventas = Ventas(id_venta, fecha, total_venta)
        return ventas

    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return None  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return None
