#Escribir un script Python que permite crear una copia (“dump”) de su base de datos.
import subprocess

#Al igual que en los otros scripts se supone un usuario root sin contraseña
username = "root"
database = "proyecto_info133"

with open('proyecto_info133.sql','w') as output:
    c = subprocess.Popen(['mysqldump', '-u',username,database],
                         stdout=output, shell=True)