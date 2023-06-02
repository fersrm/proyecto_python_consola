from validaciones import valida_numero
# librerias externas
import os # para limpiar la consola
from prettytable import PrettyTable # para crear tabla en consola

# Funciones de opciones Generales
def mostrar_mensaje_bienvenida(nombre,apellido,rol):
    # Crear la tabla
    tabla = PrettyTable()
    
    # Agregar las columnas
    tabla.field_names = ["BIENVENIDO AL SISTEMA DE VENTAS"]
    
    # Agregar el contenido de la tabla
    tabla.add_row([f"{rol}: {nombre} {apellido}"])
    
    # Personalizar el formato de la tabla
    tabla.align = "c"  # Alinear el contenido al centro
    
    # Imprimir la tabla
    print(tabla)

def pausa():
    input("#### PRESIONE ENTER PARA CONTINUAR ####")

def salir(d, s):
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
def opcion1_vendedor():
    print("Opción 1 seleccionada")

def opcion2_vendedor(a, b):
    print("Opción 2 seleccionada")

# Diccionario de opciones
menu_jefe_ventas = {
    1: (opcion1, []),
    2: (opcion2, [10, 20]),
    3: (opcion3, ["texto"]),
    4: (salir, [100, "mensaje"])
}

menu_vendedor = {
    1: (opcion1_vendedor, []),
    2: (opcion2_vendedor, [30, 40]),
    3: (salir, [200, "mensaje de salida"])
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
def iniciar_menu_jefe_ventas(nombre,apellido,rol):
    while True:
        os.system('cls')
        mostrar_mensaje_bienvenida(nombre,apellido,rol)
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
def iniciar_menu_vendedor(nombre,apellido,rol):
    while True:
        os.system('cls')
        mostrar_mensaje_bienvenida(nombre,apellido,rol)
        opciones = [
            ("1", "Opción 1"),
            ("2", "Opción 2"),
            ("3", "Salir")
        ]
        
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        ejecutar_opcion(menu_vendedor, opcion)
        pausa()
        if opcion == 3:
            break