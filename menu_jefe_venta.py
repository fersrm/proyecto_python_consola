from opciones_menu import (
    mostrar_mensaje_bienvenida,
    pausa,
    salir,
    seleccionar_opcion,
    crear_tabla
)
import os

def opcion1():
    print("Opción 1 seleccionada")

def opcion2():
    print("Opción 2 seleccionada")

def opcion3():
    print("Opción 3 seleccionada")

# Diccionario de opciones
menu_jefe_ventas = {
    1: (opcion1, []),
    2: (opcion2, []),
    3: (opcion3, []),
    4: (salir, [])
}

# Función para ejecutar la opción seleccionada del menú
def ejecutar_opcion(menu, opcion):
    # Obtener la función y los argumentos correspondientes a la opción seleccionada del diccionario
    funcion, args = menu.get(opcion, (None, None))
    if funcion:
        funcion(*args)
    else:
        print("----Opción no válida----")

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
