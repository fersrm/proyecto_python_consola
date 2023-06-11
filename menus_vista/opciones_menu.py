from controlador.validaciones import validar_numero
import os
from prettytable import PrettyTable

## Funciones generales menu ##
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

def salir(mensaje):
    os.system('cls')
    print(mensaje)

# Función para seleccionar una opción del menú o un numero
def seleccionar_opcion(mensaje):
    while True:
        numero = input(mensaje)
        numero = validar_numero(numero)

        if numero is not False:
            return numero
        print("----No es un número válido----")

# Función para crear una tabla de opciones para los menu
def crear_tabla(opciones):
    # definir los encabezados
    table = PrettyTable(["Opción", "Descripción"])   
    # Agregar filas a la tabla
    for opcion, descripcion in opciones:
        table.add_row([opcion, descripcion])   
    # Mostrar la tabla en la consola
    print(table)

# muestra tablas
def mostrar_tablas(descripcion, datos):
    tabla = PrettyTable()
    tabla.field_names = ["Número", descripcion]
    for i, dato in enumerate(datos, start=1):
        tabla.add_row([i, dato[0]])
    print(tabla)