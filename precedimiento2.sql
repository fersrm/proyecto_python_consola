DELIMITER $
-- Procedimiento almacenado para tabla para clientes
CREATE PROCEDURE traer_tablas_cliente()
BEGIN
    SELECT nombre_giro FROM tipo_giro;
    SELECT razon_social FROM razon_social WHERE id_razon_social != 1;
    SELECT nombre_comuna FROM comunas;

END$
DELIMITER ;