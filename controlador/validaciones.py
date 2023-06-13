import re  # Para expreciones regulares
from datetime import datetime # para la fechas

def validar_numero(numero):
    numero = numero.strip()
    if not numero:
        return False  # Error, el campo está vacío  
    # Verificar que sea un entero positivo y que su longitud no sea mayor a 6.
    if not numero.isdigit() or int(numero) < 0 or len(numero) > 6:
        return False # Error la validacion del numero
    return int(numero)

def validar_run(run):
    if not run:
        return False  # Error, el campo está vacío
    run = run.strip().upper()  # Normalizar el RUN
    # Verificar longitud y formato del RUN.
    if len(run) not in (9, 10) or not re.match(r'^\d{7,8}-[\dK]$', run):
        return False  # Error en la validación del RUN.
    return run  # Devolver el RUN normalizado

def validar_clave(clave):
    if not clave:
        return False  # Error, el campo está vacío  
    clave = clave.strip().upper()  # Normalizar la clave  
    # Verificar longitud y si es alfanumérica.
    if len(clave) != 8 or not clave.isalnum():
        return False  # Error en la validación de la clave.  
    return clave  # Devolver la clave normalizada

def validar_producto(dato_evaluar): # Evalúa nombre, código, marca o categoria
    if not dato_evaluar:
        return False  # Error, el campo está vacío  
    dato_evaluar = dato_evaluar.strip().upper()  # Normalizar el dato a evaluar  
    # Verificar longitud
    if len(dato_evaluar) < 2 or len(dato_evaluar) > 20:
        return False  # Error en la validación del producto  
    return dato_evaluar  # Devolver el dato normalizado

def validar_cliente(dato_evaluar): # Evalua nombre y apellido
    dato_evaluar = dato_evaluar.strip().upper()
    if not dato_evaluar:
        return False
    # verifica que solo sea letras y la longitud
    if not dato_evaluar.isalpha() or len(dato_evaluar) < 2 or len(dato_evaluar) > 25:
        return False
    return  dato_evaluar

def validar_direccion(direccion):
    direccion = direccion.strip().upper()
    if not direccion:
        return False
    # verifica la longitud
    if len(direccion) < 5 or len(direccion) > 60:
        return False
    return direccion

def validar_razon_social(razon_social):
    if not razon_social:
        return False  # Error, el campo está vacío
    razon_social = razon_social.strip().upper()  
    # Verificar longitud
    if len(razon_social) < 3 or len(razon_social) > 35:
        return False  # Error en la validación 
    return razon_social  # Devolver el dato normalizado

def validar_fecha(fecha):
    try:
        fecha = fecha.strip()
        fecha_actual = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        # Veria que la fecha sea menor a la actual
        if fecha_ingresada <= fecha_actual and fecha_ingresada.year >= 2021:
            return fecha_ingresada
        else:
            return False
    except ValueError:
        return False
