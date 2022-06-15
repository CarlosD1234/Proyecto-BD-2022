# Escribir un script Python que permite crear la estructura de la Base de datos.
import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="root",
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
cur.execute("CREATE TABLE prensa (nombre VARCHAR(255) PRIMARY KEY, url VARCHAR(255), region VARCHAR(255), pais VARCHAR(255), idioma VARCHAR(255))")
cur.execute("CREATE TABLE noticia (id INT PRIMARY KEY, url_noticia VARCHAR(255), titulo VARCHAR(255), fecha_publicacion Date, contenido MEDIUMTEXT, autor VARCHAR(255), nombre_medio VARCHAR(255), FOREIGN KEY (nombre_medio) REFERENCES prensa(nombre) )")

#cur.execute("CREATE TABLE dueño (id nombre VARCHAR(255), tipo_persona VARCHAR(255), fecha_dueño Date PRIMARY KEY(id))")
#cur.execute("CREATE TABLE referencia (url_wikipedia VARCHAR(255), id nombre_referencia VARCHAR(255), profesion VARCHAR(255), fecha_nacimiento Date, nacionalidad CHAR[250] PRIMARY KEY(id))")
#cur.execute("CREATE TABLE popularidad (fecha Date, valor INT)")
#cur.execute("CREATE TABLE propietario (nombre_prensa VARCHAR(255), nombre_dueño VARCHAR(255, fecha_dueño Date))")
#cur.execute("CREATE TABLE mencionar (url_noticia VARCHAR(255), nombre_referencia VARCHAR(255))")

conn.commit()
conn.close()