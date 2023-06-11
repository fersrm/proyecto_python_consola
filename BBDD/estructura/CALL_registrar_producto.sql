DELIMITER $
-- Procedimiento almacenado para insertar nuevo producto
CREATE PROCEDURE registro_producto(
    p_codigo_producto VARCHAR(45),
    p_nombre_producto VARCHAR(40),
    p_precio INT(6),
    p_nombre_marca VARCHAR(25),
    p_nombre_categoria VARCHAR(20),
    p_id_usuario INT
)
BEGIN
    DECLARE v_id_marca INT;
    DECLARE v_id_categoria INT;
    DECLARE v_id_producto INT;

    -- Verificar si la marca existe
    SELECT id_marca INTO v_id_marca
    FROM MARCAS
    WHERE nombre_marca = p_nombre_marca;

    -- Si la marca no existe, agregarla
    IF v_id_marca IS NULL THEN
        START TRANSACTION;
        
        INSERT INTO MARCAS (nombre_marca)
        VALUES (p_nombre_marca);

        SET v_id_marca = LAST_INSERT_ID();

        COMMIT;
    END IF;

    -- Verificar si la categoria existe
    SELECT id_categoria INTO v_id_categoria
    FROM CATEGORIAS
    WHERE nombre_categoria = p_nombre_categoria;

    -- Si la categoria no existe, agregarla
    IF v_id_categoria IS NULL THEN
        START TRANSACTION;
        
        INSERT INTO CATEGORIAS (nombre_categoria)
        VALUES (p_nombre_categoria);

        SET v_id_categoria = LAST_INSERT_ID();

        COMMIT;
    END IF;

    START TRANSACTION;

    -- Insertar el cliente en la tabla CLIENTES
    INSERT INTO PRODUCTOS (codigo_producto, nombre_producto, precio_producto, marca_FK, usuario_FK, categoria_FK) 
    VALUES (p_codigo_producto, p_nombre_producto, p_precio, v_id_marca, p_id_usuario, v_id_categoria);

    SET v_id_producto = LAST_INSERT_ID();

    COMMIT;

    SELECT p.id_producto, p.codigo_producto, p.nombre_producto, p.precio_producto, m.nombre_marca, c.nombre_categoria
    FROM PRODUCTOS AS p 
    INNER JOIN MARCAS AS m 
        ON p.marca_FK = m.id_marca 
    INNER JOIN CATEGORIAS AS c 
        ON p.categoria_FK = c.id_categoria 
    WHERE p.id_producto = v_id_producto; 

END $

DELIMITER ;
