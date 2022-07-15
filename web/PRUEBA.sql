--INSERTAR PRODUCTOS EN LA BASE DE DATOS ORACLE
INSERT INTO CORE_PRODUCTO VALUES ('aa111','Bandana Diseno', 50,1990,1,'fotos/3.jpeg');
INSERT INTO CORE_PRODUCTO VALUES ('bb222','Bandana Rosa', 50,1990,1,'fotos/4.jpg');
INSERT INTO CORE_PRODUCTO VALUES ('cc333','Bandana Reversible', 50,1990,1,'fotos/2.jpeg');
INSERT INTO CORE_PRODUCTO VALUES ('dd444','Bandana Broche', 50,1990,1,'fotos/5.png');
INSERT INTO CORE_PRODUCTO VALUES ('ee555','Correa Azul', 50,1990,1,'fotos/1.jpg');
INSERT INTO CORE_PRODUCTO VALUES ('ff666','Correa Negra', 50,1990,1,'fotos/9.png');
INSERT INTO CORE_PRODUCTO VALUES ('gg777','Correa Print', 50,1990,1,'fotos/10.webp');
INSERT INTO CORE_PRODUCTO VALUES ('hh888','Collar Mostaza', 50,1990,1,'fotos/7.jpg');
INSERT INTO CORE_PRODUCTO VALUES ('ii999','Collar Print', 50,1990,1,'fotos/8.jpg');
INSERT INTO CORE_PRODUCTO VALUES ('jj110','Correa + Arnes', 50,1990,1,'fotos/6.jpg');
INSERT INTO CORE_PRODUCTO VALUES ('kk120','Identificador NFC', 50,1990,1,'fotos/11.webp');

--INSERTAR DATOS EN ESTADO
INSERT INTO core_estado VALUES (1,'Aceptada');
INSERT INTO core_estado VALUES (2,'Preparacion');
INSERT INTO core_estado VALUES (3,'Despachada');

commit;