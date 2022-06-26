# Escribir un script Python que permite crear la estructura de la Base de datos.
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
query_create = "CREATE DATABASE proyecto_info133"
cur.execute(query_create)
cur.execute("USE proyecto_info133")
cur.execute("CREATE TABLE prensa (id_prensa INT PRIMARY KEY, nombre_prensa VARCHAR(255), url VARCHAR(255), region VARCHAR(255), pais VARCHAR(255), idioma VARCHAR(255))")
cur.execute("CREATE TABLE dueño (nombre_dueño VARCHAR(255) PRIMARY KEY, tipo_persona VARCHAR(255), fecha_dueño Date)")
cur.execute("CREATE TABLE noticia (url_noticia VARCHAR(255) PRIMARY KEY, titulo VARCHAR(255), fecha_publicacion Date, contenido MEDIUMTEXT, autor VARCHAR(255), id_prensa INT, FOREIGN KEY (id_prensa) REFERENCES prensa (id_prensa))")
cur.execute("CREATE TABLE referencia (url_wikipedia VARCHAR(255), nombre_referencia VARCHAR(255) PRIMARY KEY, profesion VARCHAR(255), fecha_nacimiento Date, nacionalidad VARCHAR(255))")
cur.execute("CREATE TABLE popularidad (id_popularidad INT PRIMARY KEY, fecha Date, valor INT, nombre_referencia VARCHAR(255), FOREIGN KEY (nombre_referencia) REFERENCES referencia (nombre_referencia))")
cur.execute("CREATE TABLE propietario (id_prensa INT, nombre_dueño VARCHAR(255), fecha_dueño Date, FOREIGN KEY (id_prensa) REFERENCES prensa (id_prensa), FOREIGN KEY (nombre_dueño) REFERENCES dueño (nombre_dueño), PRIMARY KEY (id_prensa, nombre_dueño))")
cur.execute("CREATE TABLE mencionar (url_noticia VARCHAR(255), nombre_referencia VARCHAR(255), FOREIGN KEY (url_noticia) REFERENCES noticia (url_noticia), FOREIGN KEY (nombre_referencia) REFERENCES referencia (nombre_referencia))")

conn.commit()
conn.close()