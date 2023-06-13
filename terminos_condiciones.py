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
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed pretium velit non orci hendrerit, 
                        eu ultrices enim auctor. Sed lacinia ante nec ante condimentum, a rutrum risus malesuada. Vivamus sagittis ligula
                        at nibh vestibulum ultrices. Quisque consequat lectus nec sem fermentum fringilla. Nunc eu quam eu arcu finibus 
                        interdum. Nullam eleifend augue a sem feugiat efficitur. Integer lobortis bibendum turpis id bibendum. In luctus 
                        consequat est, sit amet sagittis turpis ultrices a. Maecenas faucibus pulvinar nulla, a iaculis leo eleifend eget. 
                        Maecenas malesuada dolor ligula, ac cursus nisl laoreet nec. Sed ac nisi scelerisque, finibus tellus et, semper risus.
""")


aceptar = obtener_input_validado("Escriba 'ACEPTAR': ",validar_cliente)

if aceptar == "ACEPTAR":
    if __name__ == "__main__":
        iniciar_aplicacion()
else :
    print("----Tiene que aceptar los terminis y condiciones----")