from prettytable import PrettyTable

# Clases de usuaros del sistema y clientes
class Persona:
    def __init__(self, run, nombre, apellido, comuna, region):
        self.__run = run
        self.__nombre = nombre
        self.__apellido = apellido
        self.__comuna = comuna
        self.__region = region

    def set_run(self, run):
        self.__run = run

    def get_run(self):
        return self.__run

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_nombre(self):
        return self.__nombre

    def set_apellido(self, apellido):
        self.__apellido = apellido

    def get_apellido(self):
        return self.__apellido

    def set_comuna(self, comuna):
        self.__comuna = comuna

    def get_comuna(self):
        return self.__comuna

    def set_region(self, region):
        self.__region = region

    def get_region(self):
        return self.__region

class DatosUsuario(Persona):
    def __init__(self, run, nombre, apellido, comuna, region, rol, clave, id_rol):
        super().__init__(run, nombre, apellido, comuna, region)
        self.__rol = rol
        self.__clave = clave
        self.__id_rol = id_rol

    def set_id_rol(self, id_rol):
        self.__id_rol = id_rol

    def get_id_rol(self):
        return self.__id_rol
    
    def set_rol(self, rol):
        self.__rol = rol

    def get_rol(self):
        return self.__rol

    def set_clave(self, clave):
        self.__clave = clave

    def get_clave(self):
        return self.__clave
    
    def get_datos_usuario(self):
        return {
            "nombre": self.get_nombre(),
            "apellido": self.get_apellido(),
            "rol": self.get_rol()
        }

class DatosCliente(Persona):
    def __init__(self, run, nombre, apellido, comuna, region, razon_social, direccion, tipo_giro):
        super().__init__(run, nombre, apellido, comuna, region)
        self.__razon_social = razon_social
        self.__direccion = direccion
        self.__tipo_giro = tipo_giro

    def set_razon_social(self, razon_social):
        self.__razon_social = razon_social

    def get_razon_social(self):
        return self.__razon_social

    def set_direccion(self, direccion):
        self.__direccion = direccion

    def get_direccion(self):
        return self.__direccion

    def set_tipo_giro(self, tipo_giro):
        self.__tipo_giro = tipo_giro

    def get_tipo_giro(self):
        return self.__tipo_giro

# Clase de productos
class Producto:
    def __init__(self,id_producto, codigo_producto, nombre_producto, precio_producto, marca, categoria):
        self.__id = id_producto
        self.__codigo = codigo_producto
        self.__nombre = nombre_producto
        self.__precio = precio_producto
        self.__marca = marca
        self.__categoria = categoria

    def set_id(self, id_producto):
        self.__id = id_producto

    def get_id(self):
        return self.__id
    
    def set_codigo(self, codigo_producto):
        self.__codigo = codigo_producto

    def get_codigo(self):
        return self.__codigo

    def set_nombre(self, nombre_producto):
        self.__nombre = nombre_producto

    def get_nombre(self):
        return self.__nombre

    def set_precio(self, precio_producto):
        self.__precio = precio_producto

    def get_precio(self):
        return self.__precio

    def set_marca(self, marca):
        self.__marca = marca

    def get_marca(self):
        return self.__marca

    def set_categoria(self, categoria):
        self.__categoria = categoria

    def get_categoria(self):
        return self.__categoria

# Clases de detalle de las ventas
class Ventas:
    def __init__(self, id_venta, fecha_venta, cliente, vendedor):
        self.__id_venta = id_venta
        self.__fecha_venta = fecha_venta
        self.__cliente = cliente
        self.__vendedor = vendedor

    def set_id_venta(self, id_venta):
        self.__id_venta = id_venta

    def get_id_venta(self):
        return self.__id_venta

    def set_fecha_venta(self, fecha_venta):
        self.__fecha_venta = fecha_venta

    def get_fecha_venta(self):
        return self.__fecha_venta

    def set_cliente(self, cliente):
        self.__cliente = cliente

    def get_cliente(self):
        return self.__cliente

    def set_vendedor(self, vendedor):
        self.__vendedor = vendedor

    def get_vendedor(self):
        return self.__vendedor

class DetalleVentas:
    def __init__(self, id_detalle_venta, cantidad_productos, total_productos, id_venta):
        self.__id = id_detalle_venta
        self.__cantidad_productos = cantidad_productos
        self.__total_productos = total_productos
        self.__id_venta = id_venta

    def set_id(self, id_detalle_venta):
        self.__id = id_detalle_venta

    def get_id(self):
        return self.__id

    def set_cantidad_productos(self, cantidad_productos):
        self.__cantidad_productos = cantidad_productos

    def get_cantidad_productos(self):
        return self.__cantidad_productos

    def set_total_productos(self, total_productos):
        self.__total_productos = total_productos

    def get_total_productos(self):
        return self.__total_productos

    def set_id_venta(self, id_venta):
        self.__id_venta = id_venta

    def get_id_venta(self):
        return self.__id_venta

# Clase Facturas y boleta
class Venta:
    def __init__(self, id, total_venta, id_venta):
        self.__id = id
        self.__total_venta = total_venta
        self.__id_venta = id_venta

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_total_venta(self, total_venta):
        self.__total_venta = total_venta

    def get_total_venta(self):
        return self.__total_venta

    def set_id_venta(self, id_venta):
        self.__id_venta = id_venta

    def get_id_venta(self):
        return self.__id_venta

# Clase de datos de la empresa
class DetalleEmpresa:
    def __init__(self, nombre_local, rut_local, direccion, IVA, estado):
        self.__nombre_local = nombre_local
        self.__rut_local = rut_local
        self.__direccion = direccion
        self.__IVA = IVA
        self.__estado = estado

    def set_nombre_local(self, nombre_local):
        self.__nombre_local = nombre_local

    def get_nombre_local(self):
        return self.__nombre_local

    def set_rut_local(self, rut_local):
        self.__rut_local = rut_local

    def get_rut_local(self):
        return self.__rut_local

    def set_direccion(self, direccion):
        self.__direccion = direccion

    def get_direccion(self):
        return self.__direccion

    def set_IVA(self, IVA):
        self.__IVA = IVA

    def get_IVA(self):
        return self.__IVA

    def set_estado(self, estado):
        self.__estado = estado

    def get_estado(self):
        return self.__estado

# Clase carrito de compra
class CarritoCompra:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto, cantidad=1):
        for item in self.productos:
            if item['producto'].get_codigo() == producto.get_codigo():
                item['cantidad'] += cantidad
                return
        self.productos.append({'producto': producto, 'cantidad': cantidad})

    def actualizar_cantidad(self, codigo_producto, nueva_cantidad):
        for item in self.productos:
            if item['producto'].get_codigo() == codigo_producto:
                item['cantidad'] = nueva_cantidad
                return True
            else:
                return None

    def mostrar_detalle(self):
        if not self.productos:
            return None

        tabla = PrettyTable()
        tabla.field_names = ["Número", "Código Producto", "Nombre Producto", "Cantidad", "Precio Unitario", "Total"]

        total_carrito = 0

        for i, item in enumerate(self.productos, start=1):
            producto = item['producto']
            cantidad = item['cantidad']
            precio_unitario = producto.get_precio()
            total = cantidad * precio_unitario
            total_carrito += total

            tabla.add_row([i, producto.get_codigo(), producto.get_nombre(), cantidad, precio_unitario, total])

        tabla.add_row(["", "", "", "", "Total", total_carrito])

        return tabla

    def vaciar_carrito(self):
        self.productos = []