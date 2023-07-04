from menus_vista.opciones_menu import obtener_input_validado
from menus_vista.vista import iniciar_aplicacion
from controlador.validaciones import validar_cliente
import os

os.system('cls')


print("""
                                                   //////////////////////////////////
                                                  ///// Terminos y condiciones /////
                                                 //////////////////////////////////     
""")



print("""
        Bienvenido al sistema de ventas del “BAZAR LA NONA”, 
        antes de utilizar la aplicación solicitamos que lea detenidamente los Términos y Condiciones de Uso que componen el sistema. 
        1.-Uso no autorizado: El presente software fue desarrollado bajo fines específicos y requerimientos detallados que son especialmente vinculados 
        con los objetivos del negocio requerido por el “BAZAR LA NONA”.
        Al aceptar, usted afirma estar de acuerdo con todas las leyes y regulaciones aplicables. 
        El sistema se limita solo al personal autorizado por el negocio, quedando prohibido cualquier uso indebido por personas ajenas. 

        2.- Derechos de propiedad intelectual: El uso de esta aplicación no otorga ningún derecho adicional más allá de la autorización para su uso permitido. 
        Todos los derechos de propiedad intelectual de la aplicación pertenecen exclusivamente al equipo que desarrolló dicho software. 
        Por otra parte, ningún usuario está autorizado, en ningún caso, a realizar modificaciones en la aplicación, 
        llevar a cabo ingeniería inversa sobre la misma, 
        distribuirla, realizar copias o realizar cualquier otro uso no expresamente autorizado. 
        Cualquier incumplimiento de estas condiciones puede conllevar responsabilidades legales, incluyendo acciones penales.

        3.-Limitación de responsabilidad: En la medida permitida por la ley aplicable, no seremos responsables por daños directos, indirectos, incidentales, 
        especiales o consecuentes que puedan surgir del uso o la imposibilidad de uso de la Aplicación, 
        incluso si se nos ha notificado de la posibilidad de dichos daños, 
        esto respecto de alguna modificación o actualización realizada por personas ajenas al equipo o empresa que ha desarrollado dicho sistema.
        Los usuarios de esta aplicación aceptan expresamente, por el solo hecho de hacer uso de dicho sistema, 
        aceptando someterse y ajustarse a los términos y condiciones 
        declarados en esta sección. Al escribir “ACEPTAR” en el software, usted confirma que ha leído, 
        comprendido y aceptado de manera voluntaria con los Términos y Condiciones de Uso. En caso de no estar de acuerdo con lo anterior, 
        te pedimos que no hagas uso de él.
""")


aceptar = obtener_input_validado("Escriba 'ACEPTAR': ",validar_cliente)

if aceptar == "ACEPTAR":
    if __name__ == "__main__":
        iniciar_aplicacion()
else :
    print("----Tiene que aceptar los terminis y condiciones----")