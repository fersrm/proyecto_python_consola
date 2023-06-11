DELIMITER $
-- Procedimiento almacenado para generar una venta, boleta o factura
CREATE PROCEDURE generar_venta(p_id_cliente INT, p_id_vendedor INT, p_generar_venta INT)
BEGIN
    -- Declaracion de Variables
    DECLARE v_id_ultima_venta INT;
    DECLARE v_id_ultima_boleta INT;
    DECLARE v_id_ultima_factura INT;
    DECLARE v_total_boleta_compra INT;
    DECLARE v_total_factura_compra INT;

    -- Crear la venta
    INSERT INTO ventas (cliente_FK, usuario_FK) VALUES (p_id_cliente, p_id_vendedor);
    SET v_id_ultima_venta = LAST_INSERT_ID();

    IF p_generar_venta = 1 THEN
        -- Crear la boleta
        INSERT INTO boletas (venta_FK) VALUES (v_id_ultima_venta);
        SET v_id_ultima_boleta = LAST_INSERT_ID();

        -- Insertar detalles de la boleta desde la tabla temporal
        INSERT INTO detalle_boletas (cantidad, total, producto_FK, boleta_FK)
        SELECT cantidad, total_producto, id_producto, (v_id_ultima_boleta) AS boleta_FK FROM detalle_temp;

        -- Calcular el total de la boleta
        SELECT SUM(total_producto) INTO v_total_boleta_compra FROM detalle_temp;
        UPDATE boletas SET total_boleta = v_total_boleta_compra WHERE id_boleta = v_id_ultima_boleta;

        -- Borrar la tabla temporal
        TRUNCATE TABLE detalle_temp;

        -- Devolver la boleta creada
        SELECT b.id_boleta, b.total_boleta, DATE(v.fecha_emcion) AS fecha_emision
        FROM boletas AS b
        INNER JOIN ventas AS v ON b.venta_FK = v.id_venta
        WHERE b.id_boleta = v_id_ultima_boleta;

        -- Devolver el detalle de la boleta creada
        SELECT d.cantidad, d.total, p.codigo_producto, p.nombre_producto, p.precio_producto  
        FROM detalle_boletas AS d
        INNER JOIN productos AS p
        ON d.producto_FK = p.id_producto
        WHERE boleta_FK = v_id_ultima_boleta;

    ELSE
        -- Crear la factura
        INSERT INTO facturas (venta_FK) VALUES (v_id_ultima_venta);
        SET v_id_ultima_factura = LAST_INSERT_ID();

        -- Insertar detalles de la factura desde la tabla temporal
        INSERT INTO detalle_facturas (cantidad, total, producto_FK, factura_FK)
        SELECT cantidad, total_producto, id_producto, (v_id_ultima_factura) AS factura_FK FROM detalle_temp;

        -- Calcular el total de la factura
        SELECT SUM(total_producto) INTO v_total_factura_compra FROM detalle_temp;
        UPDATE facturas SET total_factura = v_total_factura_compra WHERE id_factura = v_id_ultima_factura;

        -- Borrar la tabla temporal
        TRUNCATE TABLE detalle_temp;

        -- Devolver la factura creada
        SELECT f.id_factura, f.total_factura, DATE(v.fecha_emcion) AS fecha_emision
        FROM facturas AS f
        INNER JOIN ventas AS v ON f.venta_FK = v.id_venta
        WHERE f.id_factura = v_id_ultima_factura;

        -- Devolver el detalle de la factura creada
        SELECT d.cantidad, d.total, p.codigo_producto, p.nombre_producto,p.precio_producto  
        FROM detalle_facturas AS d
        INNER JOIN productos AS p
        ON d.producto_FK = p.id_producto
        WHERE factura_FK = v_id_ultima_factura;

    END IF;
END$
DELIMITER ;
