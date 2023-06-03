from validaciones import valida_numero, valida_producto
from consultas import (
    obtener_datos_producto,
    buscar_producto,
    obtener_lista_productos,
)
# librerias externas
import os # para limpiar la consola
from prettytable import PrettyTable # para crear tabla en consola

# Funciones de opciones Generales
def mostrar_mensaje_bienvenida(datos_usuario):
    # Crear la tabla
    tabla = PrettyTable()
    
    # Agregar las columnas
    tabla.field_names = ["BIENVENIDO AL SISTEMA DE VENTAS"]
    
    # Agregar el contenido de la tabla
    nombre = datos_usuario["nombre"]
    apellido = datos_usuario["apellido"]
    rol = datos_usuario["rol"]
    
    tabla.add_row([f"{rol}: {nombre} {apellido}"])
    
    # Personalizar el formato de la tabla
    tabla.align = "c"  # Alinear el contenido al centro
    
    # Imprimir la tabla
    print(tabla)

def pausa():
    input("#### PRESIONE ENTER PARA CONTINUAR ####")

def salir():
    os.system('cls')
    print("Saliendo del programa")

# Funciones de opciones Menú jefe de ventas:
def opcion1():
    print("Opción 1 seleccionada")

def opcion2(a, b):
    print("Opción 2 seleccionada")

def opcion3(c):
    print("Opción 3 seleccionada")

# Funciones de opciones Menú vendedor
# Funcionabilidad registrar productos
def agregar_detalle_productos():
    print("Opción 1 seleccionada")

    # Solicitar al usuario que ingrese el nombre o código del producto
    dato_producto = input("Ingrese nombre o código: ")

    # Normalizar los datos ingresados
    dato_producto = dato_producto.strip().upper()

    # Validar el nombre o código del producto
    if not valida_producto(dato_producto):
        print("El producto ingresado no es válido")
        return False

    cantidad_producto = buscar_producto(dato_producto)

    # Verificar si se encontraron múltiples productos
    if cantidad_producto > 1:
        productos = obtener_lista_productos(dato_producto)

        if productos:
            # Mostrar tabla con los productos encontrados
            mostrar_tabla_productos(productos)

            # Solicitar al usuario que seleccione un producto por su número
            seleccion = input("Seleccione un número de producto: ")
            seleccion = valida_numero(seleccion)

            if seleccion <= len(productos):
                codigo = productos[int(seleccion) - 1]["codigo"]
                producto_seleccionado = obtener_datos_producto(codigo)
                agregar_lista_detalle(producto_seleccionado)
                print("Producto agregado al carrito")
            else:
                print("Selección inválida")
        else:
            print("No se encontraron datos para el producto especificado")
    
    # Verificar si se encontró un único producto
    elif cantidad_producto == 1:
        producto = obtener_datos_producto(dato_producto)

        if producto:
            agregar_lista_detalle(producto)
            print("Producto agregado al carrito")
        else:
            print("No se encontraron datos para el producto especificado.")
    
    # No se encontraron productos
    else:
        print("No se encontraron productos.")

def mostrar_tabla_productos(productos):
    table = PrettyTable()
    table.field_names = ["Número", "Código Producto", "Nombre Producto"]
    for i, producto in enumerate(productos, start=1):
        table.add_row([i, producto["codigo"], producto["nombre"]])
    print(table)

# Funcionabilidad mostrar carrito
carrito_compra = [] # carrito de compra
def agregar_lista_detalle(producto):
    carrito_compra.append(producto)
    return carrito_compra

def mostrar_tabla_carrito_compra(carrito_compra):
    table = PrettyTable()
    table.field_names = ["Número", "Código Producto", "Nombre Producto", "Cantidad de producto", "Precio Unitario", "Total"]

    # Diccionario para almacenar la cantidad de cada producto en el carrito
    cantidad_productos = {}
    total_carrito = 0  # Variable para calcular el total del carrito

    # Calcular la cantidad de cada producto en el carrito y calcular el total
    for producto in carrito_compra:
        codigo_producto = producto.get_codigo()
        if codigo_producto in cantidad_productos:
            cantidad_productos[codigo_producto] += 1
        else:
            cantidad_productos[codigo_producto] = 1
        total_carrito += producto.get_precio()

    # Agregar filas a la tabla con los productos y su cantidad
    productos_agregados = set()  # Conjunto para almacenar los códigos de productos agregados
    for i, producto in enumerate(carrito_compra, start=1):
        codigo_producto = producto.get_codigo()

        # Verificar si el producto ya ha sido agregado a la tabla
        if codigo_producto in productos_agregados:
            continue  # Saltar a la siguiente iteración si ya se agregó el producto

        nombre_producto = producto.get_nombre()
        cantidad_producto = cantidad_productos[codigo_producto]
        precio_unitario = producto.get_precio()
        total = cantidad_producto * precio_unitario
        table.add_row([i, codigo_producto, nombre_producto, cantidad_producto, precio_unitario, total])

        # Agregar el código del producto al conjunto de productos agregados
        productos_agregados.add(codigo_producto)

    # Agregar fila adicional para mostrar el total del carrito
    table.add_row(["", "", "", "", "Total", total_carrito])

    print(table)
    
# Funcionabilidad mostrar carrito
def ver_detalle_carrito(carrito_compra):
    print("Opción 2 seleccionada")
    if not carrito_compra:
        print("La lista de productos está vacía.")
    else:
        mostrar_tabla_carrito_compra(carrito_compra)


# Diccionario de opciones
menu_jefe_ventas = {
    1: (opcion1, []),
    2: (opcion2, [10, 20]),
    3: (opcion3, ["texto"]),
    4: (salir, [100, "mensaje"])
}

menu_vendedor = {
    1: (agregar_detalle_productos, []),
    2: (ver_detalle_carrito, [carrito_compra]),
    3: (salir, [])
}

# Función para seleccionar una opción del menú
def seleccionar_opcion(mensaje):
    while True:
        numero = input(mensaje)
        numero = valida_numero(numero)

        if numero is not False:
            return numero
        print("----No es un número válido----")

# Función para ejecutar la opción seleccionada del menú
def ejecutar_opcion(menu, opcion):
    # Obtener la función y los argumentos correspondientes a la opción seleccionada del diccionario
    funcion, args = menu.get(opcion, (None, None))
    if funcion:
        funcion(*args)
    else:
        print("Opción no válida")

# Función para crear una tabla
def crear_tabla(opciones):
    # definir los encabezados
    table = PrettyTable(["Opción", "Descripción"])
    
    # Agregar filas a la tabla
    for opcion, descripcion in opciones:
        table.add_row([opcion, descripcion])
    
    # Mostrar la tabla en la consola
    print(table)

# Función para iniciar el menú de jefe de ventas
def iniciar_menu_jefe_ventas(datos_usuario):
    while True:
        os.system('cls')
        mostrar_mensaje_bienvenida(datos_usuario)
        opciones = [
            ("1", "Opción 1"),
            ("2", "Opción 2"),
            ("3", "Opción 3"),
            ("4", "Salir")
        ]
        
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        ejecutar_opcion(menu_jefe_ventas, opcion)
        pausa()
        if opcion == 4:
            break

# Función para iniciar el menú de vendedor
def iniciar_menu_vendedor(datos_usuario):
    while True:
        os.system('cls')
        mostrar_mensaje_bienvenida(datos_usuario)
        opciones = [
            ("1", "Registro de productos"),
            ("2", "Mostrar dellate carrito"),
            ("3", "Salir")
        ]
        
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        ejecutar_opcion(menu_vendedor, opcion)
        pausa()
        if opcion == 3:
            break