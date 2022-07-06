#Escribir un script Python que permite insertar manualmente algunos datos en cada una de las tablas de la Base de datos.
from tkinter import INSERT
import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()
print("Usando como ejemplo al medio: La Estrella de Valparaiso")
cur.execute("USE proyecto_info133")
cur.execute("INSERT INTO prensa (id_prensa, nombre_prensa, url, region, pais, idioma) VALUES (8, 'La Estrella de Valparaíso', 'http://www.estrellavalpo.cl/', 'V', 'Chile', 'Español')")
cur.execute("INSERT INTO dueño (nombre_dueño, tipo_persona, fecha_dueño) VALUES ('Agustín Edwards', 'El Mercurio S.A.P', '2016-01-01')")
cur.execute("INSERT INTO noticia (url_noticia, titulo, fecha_publicacion, contenido, autor, id_prensa) VALUES ('https://www.estrellavalpo.cl/impresa/2019/10/25/full/cuerpo-principal/1/', 'Comercio porteño sufre una hecatombre', '2019-10-25', 'Portada', 'Editor', 8)")
cur.execute("INSERT INTO referencia (url_wikipedia, nombre_referencia, profesion, fecha_nacimiento, nacionalidad) VALUES ('https://es.wikipedia.org/wiki/Agust%C3%ADn_Edwards_Eastman', 'Agustín Edwards', 'Empresario', '1927-11-24', 'Chilena')")
cur.execute("INSERT INTO popularidad (id_popularidad, fecha, valor, nombre_referencia) VALUES (250, '2022-01-01', 2597, 'Agustín Edwards')")
cur.execute("INSERT INTO propietario (id_prensa, nombre_dueño, fecha_dueño) VALUES (8, 'Agustín Edwards', '2016-01-01')")
cur.execute("INSERT INTO mencionar (url_noticia, nombre_referencia) VALUES ('https://www.estrellavalpo.cl/impresa/2019/10/25/full/cuerpo-principal/1/', 'Agustín Edwards')")
conn.commit()
conn.close()