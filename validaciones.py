import re  # Para expreciones regulares

def validar_numero(numero):
    numero = numero.strip()
    if not numero:
        return False  # Error, el campo está vacío
    
    # Verificar que sea un entero positivo.
    if not numero.isdigit() or int(numero) < 0:
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

def validar_producto(dato_evaluar): # Evalúa nombre o código
    if not dato_evaluar:
        return False  # Error, el campo está vacío
    
    dato_evaluar = dato_evaluar.strip().upper()  # Normalizar el dato a evaluar
    
    # Verificar longitud
    if len(dato_evaluar) < 2:
        return False  # Error en la validación del producto
    
    return dato_evaluar  # Devolver el dato normalizado
