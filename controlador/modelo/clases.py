from prettytable import PrettyTable

# Clases de usuaros del sistema y clientes
class Persona:
    def __init__(self,id, run, nombre, apellido, comuna, region):
        self.__id = id
        self.__run = run.upper()
        self.__nombre = nombre.upper()
        self.__apellido = apellido.upper()
        self.__comuna = comuna.upper()
        self.__region = region.upper()

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id
    
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
    def __init__(self,id, run, nombre, apellido, comuna, region, rol, clave, id_rol):
        super().__init__(id, run, nombre, apellido, comuna, region)
        self.__rol = rol.upper()
        self.__clave = clave.upper()
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
            "id": self.get_id(),
            "nombre": self.get_nombre(),
            "apellido": self.get_apellido(),
            "rol": self.get_rol()
        }

class DatosCliente(Persona):
    def __init__(self,id, run, nombre, apellido, comuna, region, razon_social, direccion, tipo_giro):
        super().__init__(id, run, nombre, apellido, comuna, region)
        self.__razon_social = razon_social.upper()
        self.__direccion = direccion.upper()
        self.__tipo_giro = tipo_giro.upper()

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
    
    def mostrar_datos_cliente(self):
        tabla = PrettyTable()

        tabla.field_names = ["Datos del cliente"]
        tabla.add_row([f"Nombre: {self.get_nombre()} {self.get_apellido()} RUN: {self.get_run()}"])
        tabla.add_row([f"Direccion: {self.get_direccion()} Comuna: {self.get_comuna()} Region: {self.get_region()}"])
        tabla.add_row([f"Razon Social: {self.get_razon_social()} Tipo de giro: {self.get_tipo_giro()}"])


        return tabla

# Clase de productos
class Producto:
    def __init__(self,id_producto, codigo_producto, nombre_producto, precio_producto, marca, categoria):
        self.__id = id_producto
        self.__codigo = codigo_producto.upper()
        self.__nombre = nombre_producto.upper()
        self.__precio = precio_producto
        self.__marca = marca.upper()
        self.__categoria = categoria.upper()

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
    
    def mostrar_datos_producto(self):
        tabla = PrettyTable()
        tabla.field_names = ["Código Producto", "Nombre Producto", "Precio", "Marca", "Categoria"]

        tabla.add_row([self.get_codigo(), self.get_nombre(), self.get_precio(), self.get_marca(), self.get_categoria()])

        return tabla

# Clases de detalle de las ventas
class Ventas:
    def __init__(self, id_venta, fecha_venta, total_venta):
        self.__id_venta = id_venta
        self.__fecha_venta = fecha_venta
        self.__total_venta = total_venta

    def set_id_venta(self, id_venta):
        self.__id_venta = id_venta

    def get_id_venta(self):
        return self.__id_venta

    def set_fecha_venta(self, fecha_venta):
        self.__fecha_venta = fecha_venta

    def get_fecha_venta(self):
        return self.__fecha_venta

    def set_total_venta(self, total_venta):
        self.__total_venta = total_venta

    def get_total_venta(self):
        return self.__total_venta
    
    def mostrar_boletas(self):
        tabla_boletas = PrettyTable()
        tabla_boletas.field_names = ["Fecha", "Monto Boleta"]

        for fecha, monto_boleta in zip(self.__fecha_venta, self.__total_venta[1]):
            if monto_boleta is not None:
                tabla_boletas.add_row([fecha, monto_boleta])

        return tabla_boletas

    def mostrar_facturas(self):
        tabla_facturas = PrettyTable()
        tabla_facturas.field_names = ["Fecha", "Monto Factura"]

        for fecha, monto_factura in zip(self.__fecha_venta, self.__total_venta[0]):
            if monto_factura is not None:
                tabla_facturas.add_row([fecha, monto_factura])

        return tabla_facturas

# detalle factura o boleta (cantidad, total por producto, codigo y  nombre se guardan una lista)
class DetalleVentas:
    def __init__(self, cantidad_productos, total_productos, id_compra, total_compra, codigo_producto, nombre_producto, precio_unitario, fecha_venta):
        self.__cantidad_productos = cantidad_productos
        self.__total_productos = total_productos
        self.__id_compra = id_compra # id boleta o factura 
        self.__total_compra = total_compra
        self.__codigo_producto = codigo_producto
        self.__nombre_producto = nombre_producto
        self.__precio_unitario = precio_unitario
        self.__fecha_venta = fecha_venta

    def set_cantidad_productos(self, cantidad_productos):
        self.__cantidad_productos = cantidad_productos

    def get_cantidad_productos(self):
        return self.__cantidad_productos

    def set_total_productos(self, total_productos):
        self.__total_productos = total_productos

    def get_total_productos(self):
        return self.__total_productos

    def set_id_compra(self, id_compra):
        self.__id_compra = id_compra

    def get_id_compra(self):
        return self.__id_compra

    def set_total_compra(self, total_compra):
        self.__total_compra = total_compra

    def get_total_compra(self):
       return self.__total_compra
    
    def set_codigo_producto(self, codigo_producto):
        self.__codigo_producto = codigo_producto

    def get_codigo_producto(self):
       return self.__codigo_producto

    def set_nombre_producto(self, nombre_producto):
        self.__nombre_producto = nombre_producto

    def get_nombre_producto(self):
       return self.__nombre_producto
    
    def set_precio_unitario(self, precio_unitario):
        self.__precio_unitario = precio_unitario

    def get_precio_unitario(self):
       return self.__precio_unitario
    
    def get_fecha_venta(self):
       return self.__fecha_venta

    def mostrar_detalle_venta(self, tipo_venta, IVA):
        tabla_folio = PrettyTable()
        tabla = PrettyTable()

        tabla_folio.field_names = [f"{tipo_venta} Generada con exito"]
        tabla_folio.add_row([f"Folio: {self.get_id_compra()} Fecha: {self.get_fecha_venta()}"])

        tabla.field_names = ["Número", "Código Producto", "Nombre Producto", "Cantidad", "Precio Unitario", "Total"]

        for i, (codigo, nombre, precio, cantidad, total) in enumerate(
                zip(self.get_codigo_producto(), self.get_nombre_producto(), self.get_precio_unitario(),
                    self.get_cantidad_productos(), self.get_total_productos()), start=1):

            tabla.add_row([i, codigo, nombre, cantidad, precio, total])
        
        subtotal = self.get_total_compra()
        total_iva = round((subtotal * IVA) / 100, 2)
        total_neto = round(subtotal - total_iva, 2)

        tabla.add_row(["Total Neto: ", total_neto, f"IVA: {IVA}% ", total_iva, "Sub Total: ", subtotal])

        return tabla_folio, tabla

# Clase de datos de la empresa
class DetalleEmpresa:
    def __init__(self,id_local, nombre_local, rut_local, direccion, IVA, estado):
        self.__id_local = id_local
        self.__nombre_local = nombre_local
        self.__rut_local = rut_local
        self.__direccion = direccion
        self.__IVA = IVA
        self.__estado = estado    
        
    def get_id_local(self):
        return self.__id_local

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
    
    def mostrar_datos_empresa(self):
        tabla = PrettyTable()

        tabla.field_names = ["Datos del Local"]
        tabla.add_row([f"Nombre: {self.get_nombre_local()} RUT: {self.get_rut_local()}"])
        tabla.add_row([f"Direccion: {self.get_direccion()}"])

        return tabla

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
        if nueva_cantidad < 1:
            return False
        
        for item in self.productos:
            if item['producto'].get_codigo() == codigo_producto:
                item['cantidad'] = nueva_cantidad
                return True
        return False

    def eliminar_producto(self, codigo_producto):
        for item in self.productos:
            if item['producto'].get_codigo() == codigo_producto:
                self.productos.remove(item)
                return True
        return False

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

        tabla.add_row(["", "", "", "", "Sub Total: ", total_carrito])

        return tabla

    def vaciar_carrito(self):
        self.productos = []