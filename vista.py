from consultas import obtener_datos_usuario
from menu_vista import (
    iniciar_menu_jefe_ventas, 
    iniciar_menu_vendedor ,
    pausa
)

# librerias externas
import os # para limpiar la consola

# Funcion para pedir los datos al usuario
def login():
    user = input("Ingrese su RUN: ")
    clave = input("Ingrese su Contraseña: ")
    return user, clave

# Funcion para inciar el menu segun corresponda
def iniciar_aplicacion():
    while True:
        os.system('cls')

        user, clave = login()
        if user and clave:
            datos = obtener_datos_usuario(user, clave)
            if datos == 1:
                print("----El RUN no es válido----")
                pausa()
            elif datos == 2:
                print("----La Clave es incorrecta----")
                pausa()
            elif datos == 3:
                print("----No se encontraron datos para el usuario especificado----")
                pausa()
            elif datos == 4:
                print("----Ocurrió un error en la operación de la base de datos----")
                pausa()
            else:
                break  # Salir del bucle si no hay errores en el inicio de sesión
        else:
            print("----Error en el inicio de sesión----")
            pausa()

    datos_usuario = datos.get_datos_usuario()
    if datos.get_id_rol() == 1:
        iniciar_menu_jefe_ventas(datos_usuario)
    elif datos.get_id_rol() == 2:
        iniciar_menu_vendedor(datos_usuario)
    else:
        print("----Rol de usuario no válido----")

#--------------------------------------------
if __name__ == "__main__":
    iniciar_aplicacion()
