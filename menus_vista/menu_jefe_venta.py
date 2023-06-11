from menus_vista.opciones_menu import (
    mostrar_mensaje_bienvenida,
    pausa,
    salir,
    seleccionar_opcion,
    crear_tabla,
    mostrar_tablas
)
from controlador.consultas import (
    obtener_datos_empresa,
    buscar_producto,
    insetar_producto,
    tablas_registrar_producto
)
from controlador.validaciones import (
    validar_producto,
    validar_numero
)
import os

#------------Funcionabilidad cabiar estado------------

def cambiar_estado(datos_local):
    print("Opción 1 seleccionada")
    if datos_local:
        estado_dia = datos_local.get_estado()
    else:
        print("----No se ecnontraron datos del local----")
    # realizar cambio usar set_estado e insetar en bbdd
    print(estado_dia) # quitar esta de muestra

#------Funcionabilidad realizar informes--------------

def realizar_informes():
    print("Opción 2 seleccionada")

#------Funcionabilidad registrar nuevo producto--------

def selecionar_tabla(descripcion, elemnto_tabla):
    while True:
        respuesta = input(f"Pertenece a otra {descripcion} (s/n): ")
        if respuesta.lower() == "s":
            while True:
                dato = input(f"Ingresa la nueva {descripcion}: ")
                dato = validar_producto(dato)
                if dato:
                    return dato
                else:
                    print("----Nombre de la Marca es inválido. Inténtelo nuevamente.----")
            
        seleccion = seleccionar_opcion("Seleccione un número de la tabla: ")
        if not seleccion <= len(elemnto_tabla):
            print("----Selecion inválida----")
        else:
            dato = elemnto_tabla[seleccion - 1][0]
            return dato

def traer_datos_tabla_producto():
    marcas, categorias =  tablas_registrar_producto()
    # se nuestra la tabla de marcas
    mostrar_tablas("Marcas", marcas)
    seleccion_marca = selecionar_tabla("Marca", marcas)
    print(f"----{seleccion_marca}----")
    # se nuestra la tabla de categorias
    mostrar_tablas("Categorias", categorias)
    seleccion_categoria = selecionar_tabla("Categoria", categorias)
    print(f"----{seleccion_categoria}----")

    return seleccion_marca , seleccion_categoria

def pedir_datos_producto(codigo_producto):
    while True:
        nombre_producto = input("Ingrese el nombre del producto: ")
        nombre_producto = validar_producto(nombre_producto)
        if nombre_producto:
            break
        else:
            print("----Nombre del producto inválido. Inténtelo nuevamente.----")

    while True:
        precio = input("Ingrese el precio del producto: ")
        precio = validar_numero(precio)
        if precio:
            break
        else:
            print("----Precio inválido. Inténtelo nuevamente.----")

    marca, categoria = traer_datos_tabla_producto()
    datos_producto = [codigo_producto,nombre_producto, precio, marca, categoria]
    return datos_producto

def agregar_nuevos_productos(id_usuario):
    print("Opción 3 seleccionada")
    codigo_producto = input("Ingrese código del producto: ")
    # Normalizar y valida los datos ingresados
    codigo_producto = validar_producto(codigo_producto)
    if not codigo_producto:
        print("----El codigo ingresado no es válido----")
        return False
    existencia_producto = buscar_producto(codigo_producto)
    # Verificar si se encontraron múltiples productodato_productos
    if existencia_producto >= 1:
        print("----El producto ya existe----")
        return False
    # Comienza registro del proudcto
    os.system('cls')
    print("-----------Comenzando con el registro del Producto-----------")
    datos_nuevo_producto = pedir_datos_producto(codigo_producto)
    nuevo_producto = insetar_producto(datos_nuevo_producto, id_usuario)
    if nuevo_producto:
        os.system('cls')
        print("----Producto registrado con exito----")
        print(nuevo_producto.mostrar_datos_producto())
    else:
        print("----Error al registrar Producto----")

#------------------------------------------------------
# Diccionario de opciones
menu_jefe_ventas = {
    1: (cambiar_estado, []),
    2: (realizar_informes, []),
    3: (agregar_nuevos_productos, []),
    4: (salir, ["Saliendo del sistema"])
}

# Función para ejecutar la opción seleccionada del menú
def ejecutar_opcion_jefe_ventas(menu, opcion, datos_local, id_usuario):
    # Obtener la función y los argumentos correspondientes a la opción seleccionada del diccionario
    funcion, args = menu.get(opcion, (None, None))
    if funcion:
        if opcion == 1:
            args = [datos_local]
        elif opcion == 3:
            args = [id_usuario]
        funcion(*args)
    else:
        print("----Opción no válida----")

# Función para iniciar el menú de jefe de ventas
def iniciar_menu_jefe_ventas(datos_usuario):
    while True:
        os.system('cls')

        datos_local = obtener_datos_empresa()
        if datos_local:
            estado_dia = datos_local.get_estado()
        else:
            print("----No se ecnontraron datos del local----")
        
        if estado_dia != 1:
            estado = "Cerrado"
        else:
            estado = "Abierto"

        mostrar_mensaje_bienvenida(datos_usuario)
        opciones = [
            ("1", f"El local esta {estado} decea carbiarlo"),
            ("2", "Realizar informes"),
            ("3", "Agregar nuevos productos"),
            ("4", "Salir")
        ]
        id_usuario = datos_usuario["id"]
        
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        ejecutar_opcion_jefe_ventas(menu_jefe_ventas, opcion, datos_local, id_usuario)
        pausa()
        if opcion == 4:
            break
