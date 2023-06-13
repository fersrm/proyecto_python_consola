from menus_vista.opciones_menu import (
    mostrar_mensaje_bienvenida,
    pausa,
    salir,
    crear_tabla,
    mostrar_tablas,
    obtener_input_validado
)
from controlador.consultas import (
    obtener_datos_empresa,
    buscar_producto,
    insetar_producto,
    tablas_registrar_producto,
    generar_informe,
    obtener_datos_usuario,
    cambiar_estado_dia
)
from controlador.validaciones import (
    validar_producto,
    validar_numero,
    validar_run,
    validar_fecha
)
import os
from datetime import datetime

#------------Funcionabilidad cabiar estado------------

def cambiar_estado(datos_local):
    print("#### Opción 1 seleccionada ####")
    if not datos_local:
        print("----No se encontraron datos del local----")
        return False

    estado_dia = datos_local.get_estado()
    print(f"Estado actual del día: {'abierto' if estado_dia == 1 else 'cerrado'}")
    confirmacion = input("¿Desea cambiar el estado del día? (s/n): ")

    if confirmacion.lower() != 's':
        return False

    nuevo_estado = 2 if estado_dia == 1 else 1
    exito_cambio = cambiar_estado_dia(nuevo_estado)

    if exito_cambio:
        datos_local.set_estado(nuevo_estado)
        os.system('cls')
        print(f"El estado del día ha sido cambiado a {'abierto' if nuevo_estado == 1 else 'cerrado'}")

        if nuevo_estado == 2:
            fecha_actual = datetime.now().date()
            informe_dia = generar_informe(1, fecha_actual)

            if informe_dia:
                tabla_boletas = informe_dia.mostrar_boletas()
                tabla_facturas = informe_dia.mostrar_facturas()

                if len(tabla_boletas._rows) > 0:
                    print("Tabla de Boletas:")
                    print(tabla_boletas)

                if len(tabla_facturas._rows) > 0:
                    print("Tabla de Facturas:")
                    print(tabla_facturas)
            else:
                print("----No se encontraron datos de ventas----")
    else:
        print("Ocurrió un error al cambiar el estado en la base de datos.")
            
#------Funcionabilidad realizar informes--------------

def realizar_informe(opcion):
    if opcion == 1:
        fecha = obtener_input_validado("Ingrese la fecha que desea en formato YYYY-mm-dd: ", validar_fecha)
        ventas = generar_informe(opcion, fecha)
    else:
        run_vendedor = obtener_input_validado("Ingrese el RUN del vendedor: ", validar_run)
        datos_vendedor = obtener_datos_usuario(run_vendedor, rol= 2)
        if datos_vendedor == 3 or datos_vendedor is None:
            print("----No se encontraron datos para el usuario especificado----")
            return False
        else:
            ventas = generar_informe(opcion, datos_vendedor)
    if ventas:
        tabla_boletas = ventas.mostrar_boletas()
        tabla_facturas = ventas.mostrar_facturas()
        os.system('cls')
        if len(tabla_boletas._rows) > 0:
            print("Tabla de Boletas:")
            print(tabla_boletas)

        if len(tabla_facturas._rows) > 0:
            print("Tabla de Facturas:")
            print(tabla_facturas)
        else:
            print("No se encontraron facturas.")

    else:
        print("----No se encontraron datos----")

# Funcion para iniciar el submenu de jefe de ventas (generar informe)
def submenu_informe():
    while True:
        os.system('cls')
        print("##### Opción 2 seleccionada ####")
        opciones = [
            ("1", "Informe de ventas por Fecha"),
            ("2", "Informe de ventas por Vendedor"),
        ] 
        crear_tabla(opciones)
        opcion = obtener_input_validado("Ingrese una opción: ",validar_numero)
        if opcion in [1, 2]:
            realizar_informe(opcion)
            break
        else:
            print("----Opción no válida----")
            pausa()

#------Funcionabilidad registrar nuevo producto--------

def selecionar_tabla(descripcion, elemnto_tabla):
    while True:
        respuesta = input(f"¿Pertenece a una de estas {descripcion}? (s/n) ")
        if respuesta.lower() == "n":
            dato = obtener_input_validado(f"Ingresa la nueva {descripcion}: ", validar_producto)
            return dato
                
        seleccion = obtener_input_validado("Seleccione un número de la tabla: ",validar_numero)
        if not seleccion <= len(elemnto_tabla):
            print("----Selecion inválida----")
        else:
            dato = elemnto_tabla[seleccion - 1][0]
            return dato

def traer_datos_tabla_producto():
    marcas, categorias =  tablas_registrar_producto()
    # se nuestra la tabla de marcas
    mostrar_tablas("Marcas", marcas)
    seleccion_marca = selecionar_tabla("Marcas", marcas)
    print(f"----{seleccion_marca}----")
    # se nuestra la tabla de categorias
    mostrar_tablas("Categorias", categorias)
    seleccion_categoria = selecionar_tabla("Categorias", categorias)
    print(f"----{seleccion_categoria}----")

    return seleccion_marca , seleccion_categoria

def pedir_datos_producto(codigo_producto):
    nombre_producto = obtener_input_validado("Ingrese el nombre del producto: ", validar_producto)
    precio = obtener_input_validado("Ingrese el precio del producto: ", validar_numero)
    
    marca, categoria = traer_datos_tabla_producto()
    datos_producto = [codigo_producto, nombre_producto, precio, marca, categoria]
    return datos_producto

def agregar_nuevos_productos(id_usuario):
    print("#### Opción 3 seleccionada ####")
    codigo_producto = input("Ingrese código del producto: ")
    # Normalizar y valida los datos ingresados
    codigo_producto = validar_producto(codigo_producto)
    if not codigo_producto:
        print("----El código ingresado no es válido----")
        return False
    existencia_producto = buscar_producto(codigo_producto)
    # Verificar si se encontraron múltiples productodato_productos
    if existencia_producto >= 1:
        print("----El producto ya existe----")
        return False
    # Comienza registro del proudcto
    os.system('cls')
    print("-----------Comenzando con el registro del producto-----------")
    datos_nuevo_producto = pedir_datos_producto(codigo_producto)
    nuevo_producto = insetar_producto(datos_nuevo_producto, id_usuario)
    if nuevo_producto:
        os.system('cls')
        print("----Producto registrado con éxito----")
        print(nuevo_producto.mostrar_datos_producto())
    else:
        print("----Error al registrar producto----")

#------------------------------------------------------
# Diccionario de opciones
menu_jefe_ventas = {
    1: (cambiar_estado, []),
    2: (submenu_informe, []),
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
            print("----No se encontraron datos del local----")

        mostrar_mensaje_bienvenida(datos_usuario)
        opciones = [
            ("1", f"El local está {'abierto' if estado_dia == 1 else 'cerrado'}, ¿desea carbiarlo?"),
            ("2", "Realizar informes"),
            ("3", "Agregar nuevos productos"),
            ("4", "Salir")
        ]
        id_usuario = datos_usuario["id"]
        
        crear_tabla(opciones)
        opcion = obtener_input_validado("Ingrese una opción: ", validar_numero)
        ejecutar_opcion_jefe_ventas(menu_jefe_ventas, opcion, datos_local, id_usuario)
        pausa()
        if opcion == 4:
            break
