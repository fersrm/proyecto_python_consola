from validaciones import (
    validar_numero, 
    validar_producto
)
from consultas import (
    obtener_datos_producto,
    buscar_producto,
    obtener_lista_productos,
    generar_venta
)
from clases import CarritoCompra
import os
from prettytable import PrettyTable

# Funciones de opciones generales
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

# Funciones de opciones Menú jefe de ventas:-----------------------------------------------------------------------------------------------------------------
def opcion1():
    print("Opción 1 seleccionada")

def opcion2():
    print("Opción 2 seleccionada")

def opcion3():
    print("Opción 3 seleccionada")

# Funciones de opciones Menú vendedor:-----------------------------------------------------------------------------------------------------------------------

# Se crea instancia de carrito de compra como varible global
CARRITO = CarritoCompra()
# Funcionalidad para agregar productos al detalle de la compra: busca el producto y si lo encuentra, lo agrega. Si hay más de uno, se puede elegir.
def agregar_detalle_productos():
    print("Opción 1 seleccionada")
    # Solicitar al usuario que ingrese el nombre o código del producto
    dato_producto = input("Ingrese nombre o código del producto: ")
    # Normalizar los datos ingresados
    dato_producto = validar_producto(dato_producto)
    # Validar el nombre o código del producto
    if not dato_producto:
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
            seleccion = seleccionar_opcion("Seleccione un número de producto: ")
            if seleccion <= len(productos):
                codigo = productos[int(seleccion) - 1]["codigo"]
                producto_seleccionado = obtener_datos_producto(codigo)
                cantidad = seleccionar_opcion("Ingrese la cantidad: ")
                CARRITO.agregar_producto(producto_seleccionado, cantidad)
                print("Producto agregado al carrito")
            else:
                print("Selección inválida")
        else:
            print("No se encontraron datos para el producto especificado")
    # Verificar si se encontró un único producto
    elif cantidad_producto == 1:
        producto = obtener_datos_producto(dato_producto)
        # Mostrar tabla con el producto encontrado
        mostrar_tabla_productos([{
            "codigo": producto.get_codigo(),
            "nombre": producto.get_nombre(),
            "precio": producto.get_precio(),
        }])
        if producto:
            cantidad = seleccionar_opcion("Ingrese la cantidad: ")
            CARRITO.agregar_producto(producto, cantidad)
            print("Producto agregado al carrito")
        else:
            print("No se encontraron datos para el producto especificado.")
    # No se encontraron productos
    else:
        print("No se encontraron productos.")

# Muestra una tabla si en la busqueda se encontro mas de un producto
def mostrar_tabla_productos(productos):
    tabla = PrettyTable()
    tabla.field_names = ["Número", "Código Producto", "Nombre Producto", "Precio Producto"]
    for i, producto in enumerate(productos, start=1):
        tabla.add_row([i, producto["codigo"], producto["nombre"], producto["precio"]])
    print(tabla)
    
# Funcionabilidad mostrar detalle carrito de compra
def ver_detalle_carrito():
    print("Opción 2 seleccionada")
    detalle_carrito = CARRITO.mostrar_detalle()
    if detalle_carrito is None:
        print("El carrito de compra está vacío.")
    else:
        os.system('cls')
        print(detalle_carrito)
        submenu_carrito()

# Funcionabilidad menu carrito de compra
def editar_carrito():
    codigo_producto = input("Ingrese el codigo del producto: ").upper()
    nueva_cantidad = seleccionar_opcion("Ingrese la nueva cantidad: ")
    actualiza_cantidad = CARRITO.actualizar_cantidad(codigo_producto,nueva_cantidad)
    os.system('cls')
    detalle_carrito = CARRITO.mostrar_detalle()
    print(detalle_carrito)
    if actualiza_cantidad:
        print("Producto actualizado con exito")
    else:
        print("Error al alctualizar producto")

def vaciar_carrito():
    os.system('cls')
    CARRITO.vaciar_carrito()
    print("Carrito de compra Vaciado con exito")

def eliminar_producto():
    codigo_producto = input("Ingrese el codigo del producto: ").upper()
    eliminar_prodcuto = CARRITO.eliminar_producto(codigo_producto)
    if eliminar_prodcuto:
        print("Producto removido del carrito")
    else:
        print("Error al remover producto")
    
# Funcionabilidad  generar ventas
def generar_ventas(tipo_venta, id_vendedor):
    #--------------------------------------------------------------------
    id_cliente = 1
    #-------------------------------------------------------------------
    detalle_compra = CARRITO.productos
    if generar_venta(detalle_compra, id_cliente, id_vendedor, tipo_venta):
        CARRITO.vaciar_carrito()
        print("venta generada con exito")
    else:
        print("Error al generar la venta")

def ventas(id_vendedor):
    print("Opción 3 seleccionada")
    detalle_compra = CARRITO.productos
    if len(detalle_compra) == 0:
        print("El carrito de compra está vacío.")
    else:
        os.system('cls')
        submenu_venta(id_vendedor)

# Diccionario de opciones
menu_jefe_ventas = {
    1: (opcion1, []),
    2: (opcion2, []),
    3: (opcion3, []),
    4: (salir, [])
}

menu_vendedor = {
    1: (agregar_detalle_productos, []),
    2: (ver_detalle_carrito, []),
    4: (salir, ["Saliendo del sistema"])
}

menu_carrito = {
    1: (editar_carrito, []),
    2: (eliminar_producto, []),
    3: (vaciar_carrito, []),
    4: (salir, ["Saliendo del carrito de compra"])
}

# Función para seleccionar una opción del menú o un numero
def seleccionar_opcion(mensaje):
    while True:
        numero = input(mensaje)
        numero = validar_numero(numero)

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
            ("3", "Generar venta"),
            ("4", "Salir del sistema")
        ]
        id_vendedor = datos_usuario["id"]
        
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        if opcion == 3:
            ventas(id_vendedor) 
        else:
            ejecutar_opcion(menu_vendedor, opcion)
        pausa()
        if opcion == 4:
            break

# Función para iniciar el submenú de vendedor (carrito de compra)
def submenu_carrito():
    while True:
        opciones = [
            ("1", "Actualizar cantidad"),
            ("2", "Quitar producto"),
            ("3", "vaciar carrito"),
            ("4", "Salir del carrito")
        ]
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        ejecutar_opcion(menu_carrito, opcion)
        carrito = CARRITO.productos
        if opcion == 3 or opcion == 4 or not carrito:
            break
        else:
            pausa()
            ver_detalle_carrito()

# Función para iniciar el submenú de vendedor (generar venta)
def submenu_venta(id_vendedor):
    while True:
        os.system('cls')
        opciones = [
            ("1", "Generar Bolera"),
            ("2", "Generar Factura")
        ]
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        if opcion in [1, 2]:
            generar_ventas(opcion, id_vendedor) 
            break
        else:
            print("Opción no válida")
            pausa()
