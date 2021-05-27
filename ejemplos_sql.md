### Seleccionar los campos y indicados y cribarlos segun si son gasto y su cantidad.

SELECT fecha,concepto,cantidad
FROM movimientos
WHERE esGasto = 1 AND cantidad > 20;

************************************************************************************
### Formula para insertar datos en el texto.

INSERT INTO movimientos (categoria,fecha,concepto,esGasto,cantidad)
VALUES ("SU","2021-02-02","compra en el super",1,75)

************************************************************************************
### Para actualizar un dato utilizamos update. **OJO** con los updates, si se introducen sin un WHERE podemos cargarnos todos los valores de la tabla.

UPDATE movimientos
SET cantidad = 65
WHERE id = 8;

************************************************************************************
### Igual que en el caso anterior y aún más dramático, puedes cargarte toda la base SQL de una sola vez ¡Yujuuuu!

DELETE FROM movimientos
WHERE id = 8;