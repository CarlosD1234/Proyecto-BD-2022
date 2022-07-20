#Escribir un script Python que permite crear una copia (“dump”) de su base de datos.
import subprocess

username = "root"
password = ""
database = "proyecto_info133"

with open('proyecto_info133.sql','w') as output:
    c = subprocess.Popen(['mysqldump', '-u',username,'-p%s'%password,database],
                         stdout=output, shell=True)