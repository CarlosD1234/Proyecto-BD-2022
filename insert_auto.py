#A partir de sus scripts anteriores, automatizar los procesos para insertar datos en su base de datos.

from ctypes import sizeof
import mariadb
import sys
import random
from requests_html import HTMLSession
import w3lib.html
import html
import spacy
import wikipedia
import pageviewapi
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers import pipeline

def arreglaURL(link):
        temp = []
        for i in link:
                if(i.find('https://www.soychile.cl/valparaiso/')!=-1 and i not in temp):
                        temp.append(i)

        return temp

def agregapath(link):
        return 'https://www.soychile.cl'+link
def format_date(date):
        return(date.split("T")[0])

## Simular que estamos utilizando un navegador web
USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
session = HTMLSession()
## URL "SEED" que escrapear
URL_SEED = "https://www.soychile.cl/valparaiso/"
headers = {'user-agent':random.choice(USER_AGENT_LIST) }
response = session.get(URL_SEED,headers=headers)

####################################Se obtienen los linnks#####################
#xpath_title="//div[@class='media media-destacadas'] //a/text()"
xpath_url="//div[@class='media media-destacadas'] //a/@href"
xpath_title="//div/h1//text()" #/span
xpath_date="//div[@class='media-content-autor']//span[@class='media-fecha-modificacion']"
xpath_text="//div/div/p"

all_urls = response.html.xpath(xpath_url)
URL = [] #Dato N°1
#Se debe agregar al path del url el https://www.soychile.cl
URL +=all_urls
URL = list(map(agregapath,URL))
URL = arreglaURL(URL)   #Se arregla ya que habían links tipo: ..../valparaiso o .../quillota

# ITERAMOS EN CADA LINK Y ESCRAPEAMOS LA PÁGINA
titles = [] #Dato N°2
dates = [] #Dato N°3
texts = [] #Dato N°4
for i in URL:
        URL_SEED_UNITARY = i
        headers = {'user-agent':random.choice(USER_AGENT_LIST) }
        response = session.get(URL_SEED_UNITARY,headers=headers)
        title = response.html.xpath(xpath_title)[0]
        date = response.html.xpath(xpath_date)
        text = ""

        content = response.html.xpath(xpath_text)
        text = ""
        for index in content:
                content = index.text
                content = w3lib.html.remove_tags(content)
                content = w3lib.html.replace_escape_chars(content)
                content = html.unescape(content)
                content = content.strip()
                text=text+" "+content
        titles.append(title)
        dates.append(date)
        texts.append(text)
#print(titles)
#print(dates)
#print(texts)
#print(URL)

#Extraer las personas mencionadas
nlp = spacy.load("es_core_news_md")
personas = [] #Dato N°5
for text in texts:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PER":
            personas.append(ent.text)
#print(personas)

#Wikipedia
popularidad = [] #Dato N°6
fecha_nacimiento = [] #Dato N°7
profesion = [] #Dato N°8
urls_wikipedia = [] #Dato N°9
wikipedia.set_lang("es")
ES_MODEL_LANGUAGE="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
tokenizer_es_language = AutoTokenizer.from_pretrained(ES_MODEL_LANGUAGE)
model_es_language = AutoModelForQuestionAnswering.from_pretrained(ES_MODEL_LANGUAGE)
q_a_es = pipeline("question-answering", model=model_es_language, tokenizer=tokenizer_es_language)
for persona in personas:
    promedio_popularidad = []
    persona_mayus = str.title(persona)
    text = wikipedia.summary(persona_mayus)
    #Precauciones por si la persona no es encontrada
    try:
        result=pageviewapi.per_article('es.wikipedia', persona, '20220701', '20220705',
                            access='all-access', agent='all-agents', granularity='daily')
        var1 = q_a_es(question="¿Cuál es su profesión?", context=text)
        #print(var1["answer"])
        profesion.append(var1["answer"])
        var2 = q_a_es(question="¿Cuál es su fecha de nacimiento?", context=text)
        #print(var2["answer"])
        fecha_nacimiento.append(var2["answer"])
        for item in result.items():
            for article in item[1]:
                timestamp = article['timestamp']
                views = article['views']
                #print(timestamp, views)
                promedio_popularidad.append(views)
        promedio_popularidad = sum(promedio_popularidad)/len(promedio_popularidad)
        popularidad.append(promedio_popularidad)
        urls_wikipedia.append(wikipedia.page(persona_mayus).url)
    except:
        print("Página no encontrada")

print(popularidad)
print(fecha_nacimiento)
print(profesion)
print(urls_wikipedia)
#Arreglamos las fechas obtenidas anteriormente para que sean de la forma YYYY-MM-DD
formato_fecha = [] #Dato N°7 pero arreglado
for fecha in fecha_nacimiento:
    text=""
    fecha_por_partes = fecha.split(" ")
    #Año
    text=text+fecha_por_partes[4]+"-"
    #Mes
    if "enero" == fecha_por_partes[2]:
        text=text+"01-"
    elif "febrero" == fecha_por_partes[2]:
        text=text+"02-"
    elif "marzo" == fecha_por_partes[2]:
        text=text+"03-"
    elif "abril" == fecha_por_partes[2]:
        text=text+"04-"
    elif "mayo" == fecha_por_partes[2]:
        text=text+"05-"
    elif "junio" == fecha_por_partes[2]:
        text=text+"06-"
    elif "julio" == fecha_por_partes[2]:
        text=text+"07-"
    elif "agosto" == fecha_por_partes[2]:
        text=text+"08-"
    elif "septiembre" == fecha_por_partes[2]:
        text=text+"09-"
    elif "octubre" == fecha_por_partes[2]:
        text=text+"10-"
    elif "noviembre" == fecha_por_partes[2]:
        text=text+"11-"
    elif "diciembre" == fecha_por_partes[2]:
        text=text+"12-"
    #Día
    if len(fecha_por_partes[0]) == 1:
        text=text+"0"+fecha_por_partes[0]
    else:
        text=text+fecha_por_partes[0]
    formato_fecha.append(text)
print(formato_fecha)

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

# INSERTAR DATO 1-4
for i in range (len(titles)): 
    cur.execute("INSERT INTO noticia (url_noticia, titulo, fecha_publicacion, contenido, autor, id_prensa) VALUES ('%s', '%s', '%s', '%s', 'EDITOR', 8)"%(URL[i], titles[i], '2000-01-01', texts[i]))

# INSERTAR DATO 5-9
for i in range (len(personas)):
    cur.execute("INSERT INTO referencia (url_wikipedia, nombre_referencia, profesion, fecha_nacimiento, nacionalidad) VALUES ('%s', '%s', '%s', '%s', '%s')"%(urls_wikipedia[i], personas[i], profesion[i], formato_fecha[i], 'Chile'))
    cur.execute("INSERT INTO popularidad (id_popularidad, fecha, valor, nombre_referencia) VALUES ('%s', '%s', '%s', '%s')"%(i, formato_fecha[i], popularidad[i], personas[i]))
    cur.execute("INSERT INTO mencionar (url_noticia, nombre_referencia) VALUES ('%s', '%s')"%(URL[i], personas[i]))
