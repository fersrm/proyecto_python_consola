from validaciones import valida_numero, valida_producto
from consultas import (
    obtener_datos_producto,
    buscar_producto,
    obtener_lista_productos,
)
from clases import CarritoCompra
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

# Se crea instancia de carrito de compra
carrito = CarritoCompra()
# Funcionabilidad agregar productos al detalle de la compra : busca el prodcuto y si lo encuenta lo agrega, si ahi mas de uno a a eleguir
def agregar_detalle_productos():
    print("Opción 1 seleccionada")

    # Solicitar al usuario que ingrese el nombre o código del producto
    dato_producto = input("Ingrese nombre o código del producto: ")

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
                cantidad = seleccionar_opcion("Ingrese la cantidad : ")
                carrito.agregar_producto(producto_seleccionado, cantidad)
                print("Producto agregado al carrito")
            else:
                print("Selección inválida")
        else:
            print("No se encontraron datos para el producto especificado")
    
    # Verificar si se encontró un único producto
    elif cantidad_producto == 1:
        producto = obtener_datos_producto(dato_producto)

        if producto:
            cantidad = seleccionar_opcion("Ingrese la cantidad : ")
            carrito.agregar_producto(producto, cantidad)
            print("Producto agregado al carrito")
        else:
            print("No se encontraron datos para el producto especificado.")
    
    # No se encontraron productos
    else:
        print("No se encontraron productos.")
# Muestra una tabla si en la busqueda se encontro mas de un producto
def mostrar_tabla_productos(productos):
    table = PrettyTable()
    table.field_names = ["Número", "Código Producto", "Nombre Producto"]
    for i, producto in enumerate(productos, start=1):
        table.add_row([i, producto["codigo"], producto["nombre"]])
    print(table)
    
# Funcionabilidad mostrar carrito de compra
def ver_detalle_carrito():
    print("Opción 2 seleccionada")
    carrito.mostrar_detalle()
    ### agregar submenu de opciones del carrito ### "actualizar y vaciar"

# Diccionario de opciones
menu_jefe_ventas = {
    1: (opcion1, []),
    2: (opcion2, [10, 20]),
    3: (opcion3, ["texto"]),
    4: (salir, [100, "mensaje"])
}

menu_vendedor = {
    1: (agregar_detalle_productos, []),
    2: (ver_detalle_carrito, []),
    3: (salir, [])
}

# Función para seleccionar una opción del menú o un numero
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

# Función para crear una tabla de opciones para los menu
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