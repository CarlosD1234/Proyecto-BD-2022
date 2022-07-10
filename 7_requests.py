#Escribir un script Python que permite consultar la base de datos para responder a las consultas siguientes:
#¿Cuántas noticias fueron publicadas por cada medio de prensa?
#¿Quienes son las personas mencionadas en las noticias de un día específico?
#¿Cómo evoluciona la popularidad de una persona específica?
#¿Cuáles son los 5 medios de prensa más antiguos en una región especifica?

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
cur.execute("USE proyecto_info133")
cur.execute("SELECT p.nombre_prensa, COUNT(*) FROM noticia n JOIN prensa p ON n.id_prensa = p.id_prensa GROUP BY p.nombre_prensa")
cur.execute("SELECT n.nombre_referencia, m.fecha_publicacion FROM noticia m JOIN mencionar n ON m.url_noticia = n.url_noticia WHERE m.fecha_publicacion = '2019-07-08'")
cur.execute("SELECT AVG(p.valor), p.nombre_referencia FROM popularidad p JOIN referencia n ON p.nombre_referencia = n.nombre_referencia WHERE p.nombre_referencia='John Doe'")
cur.execute("SELECT p.nombre_prensa, d.fecha_dueño, p.region FROM prensa p JOIN propietario d ON p.id_prensa = d.id_prensa WHERE p.region='V' ORDER BY d.fecha_dueño ASC LIMIT 5")