DELIMITER $
-- Procedimiento almacenado para tabla para clientes
CREATE PROCEDURE traer_tablas_producto()
BEGIN
    SELECT nombre_marca FROM marcas;
    SELECT nombre_categoria FROM categorias;
END$
DELIMITER ;