from conexion import Conexion, pymysql
from clases import DatosUsuario
from validaciones import valida_run, valida_clave

# Funciones de consultas SQL
def obtener_datos_usuario(run, clave):
    try:
        # Normalizo los datos
        run = run.upper()  
        clave = clave.upper()
        # Validación de RUN y clave
        if not valida_run(run): 
            return 1
        if not valida_clave(clave):
            return 2 
        # Consulta a la base de datos
        with Conexion() as conexion:
            cursor = conexion.get_cursor()
            sql_query = ("SELECT u.run_usuario, u.clave_usuario, u.nombre_usuario, u.apellido_usuario, u.rol_FK, rol.rol_usuario, c.nombre_comuna, r.nombre_region "
                        "FROM USUARIOS AS u "
                        "INNER JOIN ROLES AS rol "
                            "ON u.rol_FK = rol.id_rol "
                        "INNER JOIN COMUNAS AS c "
                            "ON u.comuna_FK = c.id_comuna "
                        "INNER JOIN REGIONES AS r "
                            "ON c.region_FK = r.id_regiones "
                        "WHERE u.run_usuario = %s AND u.clave_usuario = %s")
            cursor.execute(sql_query, (run, clave))
            datos = cursor.fetchone()
        # Se guardan los datos
        if datos:
            run_user = datos[0].upper()
            clave_user = datos[1].upper()
            nombre_user = datos[2].upper()
            apellido_user = datos[3].upper()
            id_rol_usur = datos[4]
            rol_user = datos[5].upper()
            comuna_user = datos[6].upper()
            region_user = datos[7].upper()
            # Se crea una intancia con los datos
            user = DatosUsuario(run_user, nombre_user, apellido_user, comuna_user, region_user, rol_user, clave_user,id_rol_usur)
            return user

        return 3  # No se encontraron datos para el usuario especificado.
    except pymysql.err.Error as error:
        print(f"Error de base de datos: {error}")
        return 4  # Ocurrió un error en la operación de la base de datos.
    except Exception as error:
        print(f"Error desconocido: {error}")
        return 4  # Ocurrió un error en la operación de la base de datos.

