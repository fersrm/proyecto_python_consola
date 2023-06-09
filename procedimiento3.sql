DELIMITER $
-- Procedimiento almacenado para insertar nuevo cliente
CREATE PROCEDURE registro_cliente(
    p_run_cliente VARCHAR(10),
    p_nombre_cliente VARCHAR(25),
    p_apellido_cliente VARCHAR(25),
    p_direccion VARCHAR(64),
    p_nombre_giro VARCHAR(30),
    p_razon_social VARCHAR(45),
    p_nombre_comuna VARCHAR(30),
    p_id_vendedor INT
)
BEGIN
    DECLARE v_id_comuna INT;
    DECLARE v_id_giro INT;
    DECLARE v_id_razon_social INT;
    DECLARE v_id_cliente INT;

    -- Obtener el ID de la comuna
    SELECT id_comuna INTO v_id_comuna
    FROM COMUNAS
    WHERE nombre_comuna = p_nombre_comuna;

    -- Obtener el ID del giro
    SELECT id_giro INTO v_id_giro
    FROM TIPO_GIRO
    WHERE nombre_giro = p_nombre_giro;

    -- Verificar si la razón social existe
    SELECT id_razon_social INTO v_id_razon_social
    FROM RAZON_SOCIAL
    WHERE razon_social = p_razon_social;

    -- Si la razón social no existe, agregarla
    IF v_id_razon_social IS NULL THEN
        START TRANSACTION;
        
        INSERT INTO RAZON_SOCIAL (razon_social)
        VALUES (p_razon_social);

        SET v_id_razon_social = LAST_INSERT_ID();

        COMMIT;
    END IF;

    START TRANSACTION;

    -- Insertar el cliente en la tabla CLIENTES
    INSERT INTO CLIENTES (run_cliente, nombre_cliente, apellido_cliente, direccion, comuna_FK, tipo_giro_FK, razon_social_FK, usuario_FK)
    VALUES (p_run_cliente, p_nombre_cliente, p_apellido_cliente, p_direccion, v_id_comuna, v_id_giro, v_id_razon_social, p_id_vendedor);

    SET v_id_cliente = LAST_INSERT_ID();

    COMMIT;

    SELECT cl.id_cliente, cl.run_cliente, cl.nombre_cliente, cl.apellido_cliente, e.razon_social, t.nombre_giro, cl.direccion, c.nombre_comuna, r.nombre_region 
    FROM CLIENTES AS cl 
    INNER JOIN RAZON_SOCIAL AS e 
        ON cl.razon_social_FK = e.id_razon_social 
    INNER JOIN TIPO_GIRO AS t 
        ON cl.tipo_giro_FK = t.id_giro 
    INNER JOIN COMUNAS AS c 
        ON cl.comuna_FK = c.id_comuna 
    INNER JOIN REGIONES AS r 
        ON c.region_FK = r.id_regiones 
    WHERE cl.id_cliente = v_id_cliente;
END $

DELIMITER ;
