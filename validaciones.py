import re  # Para expreciones regulares

def valida_numero(numero):
    numero = numero.strip()
    if not numero:
        return False  # Error, el campo está vacío
    
    # Verificar que sea un entero positivo.
    if not numero.isdigit() or int(numero) < 0:
        return False # Error la validacion del numero
    
    return int(numero)

def valida_run(run):
    if not run:
        return False  # Error, el campo está vacío
    
    # Verificar longitud y formato del RUN.
    if len(run) not in (9, 10) or not re.match(r'^\d{7,8}-[\dK]$', run):
        return False # Error la validacion del RUN.
    
    return True

def valida_clave(clave):
    if not clave:
        return False  # Error, el campo está vacío
    
    # Verificar longitud y si es alfanumérica.
    if len(clave) != 8 or not clave.isalnum():
        return False  # Error la validacion de la clave.
    
    return True

def valida_producto(dato_evaluar): # Evalua nombre o codigo
    if not dato_evaluar:
        return False  # Error, el campo está vacío
    
    # Verificar longitud
    if len(dato_evaluar) < 2:
        return False  # Error la validacion del producto
    
    return True