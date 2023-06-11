from controlador.validaciones import (
    validar_producto,
    validar_cliente,
    validar_direccion,
    validar_razon_social
)
from controlador.consultas import (
    obtener_datos_producto,
    buscar_producto,
    obtener_lista_productos,
    obtener_datos_Cliente,
    generar_venta,
    tablas_registrar_cliente,
    insertar_cliente,
    obtener_datos_empresa
)
from menus_vista.opciones_menu import (
    mostrar_mensaje_bienvenida,
    pausa,
    salir,
    seleccionar_opcion,
    crear_tabla
)
from controlador.clases import CarritoCompra
import os
from prettytable import PrettyTable

## Funciones menu vendedor ##--------------------------------------------------------------------------------------------------

# Funcionalidad para agregar productos al detalle de la compra: busca el producto y si lo encuentra, lo agrega. Si hay más de uno, se puede elegir.
def agregar_detalle_productos(carrito):
    print("#### Opción 1 seleccionada ####")
    # Solicitar al usuario que ingrese el nombre o código del producto
    dato_producto = input("Ingrese nombre o código del producto: ")
    # Normalizar los datos ingresados
    dato_producto = validar_producto(dato_producto)
    # Validar el nombre o código del producto
    if not dato_producto:
        print("----El producto ingresado no es válido----")
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
                codigo = productos[seleccion - 1]["codigo"]
                producto_seleccionado = obtener_datos_producto(codigo)
                cantidad = seleccionar_opcion("Ingrese la cantidad: ")
                carrito.agregar_producto(producto_seleccionado, cantidad)
                print("----Producto agregado al carrito----")
            else:
                print("----Selección inválida----")
        else:
            print("----No se encontraron datos para el producto especificado----")
    # Verificar si se encontró un único producto
    elif cantidad_producto == 1:
        producto = obtener_datos_producto(dato_producto)
        if producto:
            # Mostrar tabla con el producto encontrado
            mostrar_tabla_productos([{
                "codigo": producto.get_codigo(),
                "nombre": producto.get_nombre(),
                "precio": producto.get_precio(),
            }])
            cantidad = seleccionar_opcion("Ingrese la cantidad: ")
            carrito.agregar_producto(producto, cantidad)
            print("----Producto agregado al carrito----")
        else:
            print("----No se encontraron datos para el producto especificado.----")
    # No se encontraron productos
    else:
        print("----No se encontraron productos.----")

# Muestra una tabla si en la busqueda se encontro mas de un producto
def mostrar_tabla_productos(productos):
    tabla = PrettyTable()
    tabla.field_names = ["Número", "Código Producto", "Nombre Producto", "Precio Producto"]
    for i, producto in enumerate(productos, start=1):
        tabla.add_row([i, producto["codigo"], producto["nombre"], producto["precio"]])
    print(tabla)
    
# Funcionabilidad mostrar detalle carrito de compra llama submenu del carrito
def ver_detalle_carrito(carrito):
    print("#### Opción 2 seleccionada ####")
    if not carrito.productos:
        print("----El carrito de compra está vacío.----")
    else:
        os.system('cls')
        submenu_carrito(carrito)

# Funcionabilidad para generar selecionar boleta o factura llama submenu venta
def ventas(carrito, id_vendedor, datos_local):
    print("#### Opción 3 seleccionada ####")
    if not carrito.productos:
        print("----El carrito de compra está vacío.----")
    else:
        os.system('cls')
        submenu_venta(id_vendedor, carrito , datos_local)

## Funciones de los Submenu ##--------------------------------------------------------------------------------------------------

# Funcionabilidad carrito de compra (submenu_carrito)
def editar_carrito(carrito):
    codigo_producto = input("Ingrese el codigo del producto: ").upper()
    nueva_cantidad = seleccionar_opcion("Ingrese la nueva cantidad: ")
    actualiza_cantidad = carrito.actualizar_cantidad(codigo_producto,nueva_cantidad)
    os.system('cls')
    detalle_carrito = carrito.mostrar_detalle()
    print(detalle_carrito)
    if actualiza_cantidad:
        print("----Producto actualizado con exito----")
    else:
        print("----Error al alctualizar producto----")

def eliminar_producto(carrito):
    codigo_producto = input("Ingrese el codigo del producto: ").upper()
    eliminar_prodcuto = carrito.eliminar_producto(codigo_producto)
    os.system('cls')
    detalle_carrito = carrito.mostrar_detalle()
    print(detalle_carrito)
    if eliminar_prodcuto:
        print("----Producto removido del carrito----")
    else:
        print("----Error al remover producto----")

def vaciar_carrito(carrito):
    os.system('cls')
    carrito.vaciar_carrito()
    print("----Carrito de compra Vaciado con exito----")
    
# Funcionabilidad registrar cliente
def mostrar_tabla_clienta(descripcion, datos):
    tabla = PrettyTable()
    tabla.field_names = ["Número", descripcion]
    for i, dato in enumerate(datos, start=1):
        tabla.add_row([i, dato[0]])
    print(tabla)

def traer_datos_tabla_cliente():
    tipo_griro, razon_socail, comunas =  tablas_registrar_cliente()
    # se nuestra la tabla de tipos de giro
    mostrar_tabla_clienta("Tipo de giro", tipo_griro)
    seleccion_giro = selecionar_tabla("Tipo de giro", tipo_griro)
    print(seleccion_giro)
    # se nuestra la tabla de razon social si es necesario
    seleccion_razon = "NO TIENE"
    seleccionar_razon_social = input("¿Desea seleccionar una razón social? (s/n): ")
    if seleccionar_razon_social.lower() == "s":
        mostrar_tabla_clienta("Razon social", razon_socail)
        seleccion_razon = selecionar_tabla("Razon social", razon_socail)
        print(seleccion_razon)
    # se nuestra la tabla de las comunas
    mostrar_tabla_clienta("Comuna", comunas)
    seleccion_comuna = selecionar_tabla("Comuna", comunas)
    print(seleccion_comuna)

    return seleccion_giro, seleccion_razon , seleccion_comuna

def selecionar_tabla(descripcion, elemnto_tabla):
    while True:
        if descripcion == "Razon social":
            respuesta = input("Pertenece a otra : Razon social. (s/n): ")
            if respuesta.lower() == "s":
                dato = input("Ingresa la Razon social: ")
                dato = validar_razon_social(dato)
                return dato
        seleccion = seleccionar_opcion("Seleccione un número de la tabla: ")
        if not seleccion <= len(elemnto_tabla):
            print("----Selecion inválida----")
        else:
            dato = elemnto_tabla[seleccion - 1][0]
            return dato

def registrar_cliente(run_cliente):
    while True:
        nombre = input("Ingrese el nombre del cliente: ")
        nombre = validar_cliente(nombre)
        if nombre:
            break
        else:
            print("----Nombre inválido. Inténtelo nuevamente.----")

    while True:
        apellido = input("Ingrese el apellido del cliente: ")
        apellido = validar_cliente(apellido)
        if apellido:
            break
        else:
            print("----Apellido inválido. Inténtelo nuevamente.----")

    while True:
        direccion = input("Ingrese la dirección del cliente: ")
        direccion = validar_direccion(direccion)
        if direccion:
            break
        else:
            print("----Dirección inválida. Inténtelo nuevamente.----")

    giro, razon, comuna = traer_datos_tabla_cliente()
    datos_cliente = [run_cliente, nombre, apellido, direccion, giro, razon, comuna]
    return datos_cliente

# Funcionabilidad  generar ventas (Submenu_venta)
def generar_ventas(tipo_venta, id_vendedor, carrito, datos_local):
    while True:
        run_cliente = input("Ingrese el RUN del cliente: ")
        datos_cliente = obtener_datos_Cliente(run_cliente)
        # Resultado consulta, pide registro de cliente si no esta en la BBDD
        if datos_cliente == 1:
            print("----El RUN no es válido----")
        elif datos_cliente == 2:
            os.system('cls')
            print("----No se encontraron datos para el cliente especificado----")
            print("-----------Comenzando con el registro del Cliente-----------")# ver si preguntar o de forma directa
            cliente = registrar_cliente(run_cliente)
            if not cliente:
                print("----Error: No se pudo registrar al cliente. Verifique los datos ingresados.----")
            else:
                datos_cliente = insertar_cliente(cliente, id_vendedor)
                if datos_cliente:
                    print("----Cliente registrado con éxito.----")
                    break
                else:
                    print("----Error: No se pudo insertar el cliente en la base de datos.----")
                    return
        elif datos_cliente == 3:
            print("----Ocurrió un error en la operación de la base de datos----")
            return
        else:
            break
    # Cuando ya se tiene la instancia del cliente se procese con la venta
    id_cliente = datos_cliente.get_id()
    detalle_compra = carrito.productos
    resultado_venta = generar_venta(detalle_compra, id_cliente, id_vendedor, tipo_venta)
    # se imprime la boleta o factura y se vacea el carrito
    if resultado_venta:
        carrito.vaciar_carrito()
        os.system('cls')
        # datos local
        if datos_local:
            IVA = datos_local.get_IVA()
            print(datos_local.mostrar_datos_empresa())
        else:
            print("----No se ecnontraron datos del local----")
            IVA = 19
        if tipo_venta == 1:
            tipo = "Boleta"
        elif tipo_venta == 2:
            tabla_cliente = datos_cliente.mostrar_datos_cliente()
            print(tabla_cliente)
            tipo = "Factura"

        tabla_folio, tabla_detalle = resultado_venta.mostrar_detalle_venta(tipo, IVA)
        print(tabla_folio)
        print(tabla_detalle)
    else:
        print("----Error al generar la venta. Inténtelo nuevamente.----")

## Diccionario de opciones ##------------------------------------------------------------------------------------------------------

menu_vendedor = {
    1: (agregar_detalle_productos, []),
    2: (ver_detalle_carrito, []),
    3: (ventas, []),
    4: (salir, ["Saliendo del sistema"])
}

menu_carrito = {
    1: (editar_carrito, []),
    2: (eliminar_producto, []),
    3: (vaciar_carrito, []),
    4: (salir, ["Saliendo del carrito de compra"])
}

# Función para ejecutar la opción seleccionada del menú
def ejecutar_opcion_vendedor(menu, opcion, carrito, id_vendedor, datos_local):
    # Obtener la función y los argumentos correspondientes a la opción seleccionada del diccionario
    funcion, args = menu.get(opcion, (None, None))
    if funcion:
        if opcion == 3:
            args = [carrito, id_vendedor, datos_local]
        elif opcion != 4:
            args = [carrito]
        funcion(*args)
    else:
        print("----Opción no válida----")

def ejecutar_opcion_carrito(menu, opcion, carrito):
    # Obtener la función y los argumentos correspondientes a la opción seleccionada del diccionario
    funcion, args = menu.get(opcion, (None, None))
    if funcion:
        if opcion != 4:
            args = [carrito]
        funcion(*args)
    else:
        print("----Opción no válida----")

# Función para iniciar el menú de vendedor
def iniciar_menu_vendedor(datos_usuario):
    carrito = CarritoCompra()
    while True:
        os.system('cls')
        
        datos_local = obtener_datos_empresa()
        if datos_local:
            estado_dia = datos_local.get_estado()
        else:
            print("----No se ecnontraron datos del local----")

        mostrar_mensaje_bienvenida(datos_usuario)
        if estado_dia != 1:
            print("----El local se encuentra cerrado----")
            break

        opciones = [
            ("1", "Registro de productos"),  # pasar carrito
            ("2", "Mostrar detalle carrito"),  # pasar carrito
            ("3", "Generar ventas"),  # pasar carrito , id_vendedor y del local
            ("4", "Salir del sistema")
        ]
        id_vendedor = datos_usuario["id"]

        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        ejecutar_opcion_vendedor(menu_vendedor, opcion, carrito, id_vendedor, datos_local)  # Pasar los parámetros correspondientes
        pausa()
        if opcion == 4:
            break

# Función para iniciar el submenú de vendedor (carrito de compra)
def submenu_carrito(carrito):
    while True:
        os.system('cls')
        if not carrito.productos:
            break
        detalle_carrito = carrito.mostrar_detalle()
        print(detalle_carrito)
        opciones = [
            ("1", "Actualizar cantidad"),
            ("2", "Quitar producto"),
            ("3", "Vaciar carrito"),
            ("4", "Salir del carrito")
        ]
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")

        ejecutar_opcion_carrito(menu_carrito, opcion, carrito)  # Pasar los parámetros correspondientes
        if opcion == 4 or opcion == 3:
            break
        pausa()

# Función para iniciar el submenú de vendedor (generar venta)
def submenu_venta(id_vendedor, carrito, datos_local):
    while True:
        os.system('cls')
        print("#### Opción 3 seleccionada ####")
        opciones = [
            ("1", "Generar Boleta"),
            ("2", "Generar Factura")
        ]
        crear_tabla(opciones)
        opcion = seleccionar_opcion("Ingrese una opción: ")
        if opcion in [1, 2]:
            generar_ventas(opcion, id_vendedor, carrito, datos_local) 
            break
        else:
            print("----Opción no válida----")
            pausa()
