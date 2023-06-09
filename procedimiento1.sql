DELIMITER $
-- Procedimiento almacenado para generar una venta, boleta o factura
CREATE PROCEDURE generar_venta(id_cliente INT, id_vendedor INT, generar_venta INT)
BEGIN
    -- Declaracion de Variables
    DECLARE id_ultima_venta INT;
    DECLARE id_ultima_boleta INT;
    DECLARE id_ultima_factura INT;
    DECLARE total_boleta_compra INT;
    DECLARE total_factura_compra INT;

    -- Crear la venta
    INSERT INTO ventas (cliente_FK, usuario_FK) VALUES (id_cliente, id_vendedor);
    SET id_ultima_venta = LAST_INSERT_ID();

    IF generar_venta = 1 THEN
        -- Crear la boleta
        INSERT INTO boletas (venta_FK) VALUES (id_ultima_venta);
        SET id_ultima_boleta = LAST_INSERT_ID();

        -- Insertar detalles de la boleta desde la tabla temporal
        INSERT INTO detalle_boletas (cantidad, total, producto_FK, boleta_FK)
        SELECT cantidad, total_producto, id_producto, (id_ultima_boleta) AS boleta_FK FROM detalle_temp;

        -- Calcular el total de la boleta
        SELECT SUM(total_producto) INTO total_boleta_compra FROM detalle_temp;
        UPDATE boletas SET total_boleta = total_boleta_compra WHERE id_boleta = id_ultima_boleta;

        -- Borrar la tabla temporal
        TRUNCATE TABLE detalle_temp;

        -- Devolver la boleta creada
        SELECT id_boleta, total_boleta FROM boletas WHERE id_boleta = id_ultima_boleta;

        -- Devolver el detalle de la boleta creada
        SELECT d.cantidad, d.total, p.codigo_producto, p.nombre_producto, p.nombre_producto,p.precio_producto  
        FROM detalle_boletas AS d
        INNER JOIN productos AS p
        ON d.producto_FK = p.id_producto
        WHERE boleta_FK = id_ultima_boleta;

    ELSE
        -- Crear la factura
        INSERT INTO facturas (venta_FK) VALUES (id_ultima_venta);
        SET id_ultima_factura = LAST_INSERT_ID();

        -- Insertar detalles de la factura desde la tabla temporal
        INSERT INTO detalle_facturas (cantidad, total, producto_FK, factura_FK)
        SELECT cantidad, total_producto, id_producto, (id_ultima_factura) AS factura_FK FROM detalle_temp;

        -- Calcular el total de la factura
        SELECT SUM(total_producto) INTO total_factura_compra FROM detalle_temp;
        UPDATE facturas SET total_factura = total_factura_compra WHERE id_factura = id_ultima_factura;

        -- Borrar la tabla temporal
        TRUNCATE TABLE detalle_temp;

        -- Devolver la factura creada
        SELECT id_factura, total_factura FROM facturas WHERE id_factura = id_ultima_factura;

        -- Devolver el detalle de la factura creada
        SELECT d.cantidad, d.total, p.codigo_producto, p.nombre_producto, p.nombre_producto,p.precio_producto  
        FROM detalle_facturas AS d
        INNER JOIN productos AS p
        ON d.producto_FK = p.id_producto
        WHERE factura_FK = id_ultima_factura;

    END IF;
END$
DELIMITER ;
