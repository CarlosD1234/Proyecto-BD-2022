#Escribir varios scripts Python que permiten “escrapear” automáticamente algunas noticias de prensa publicadas en los medios de prensa de la región, conservando en particular el URL, la fecha de publicación, el título, el texto de la noticia.
import random
from requests_html import HTMLSession
import w3lib.html
import html

def format_mes(mes):
        if(mes == "enero"):
                return "01"
        if(mes == "febrero"):
                return "02"
        if(mes == "marzo"):
                return "03"
        if(mes == "abril"):
                return "04"
        if(mes == "mayo"):
                return "05"
        if(mes == "junio"):
                return "06"
        if(mes == "julio"):
                return "07"
        if(mes == "agosto"):
                return "08"
        if(mes == "septiembre"):
                return "09"
        if(mes == "octubre"):
                return "10"
        if(mes == "noviembre"):
                return "11"
        if(mes == "diciembre"):
                return "12"



def format_date_casero(date):
        # martes 12 julio de 2022 | Publicado a las 10:03 pm · Actualizado a las 10:03 pm
        # DEBE QUEDAR => 2022-07-18
        date = date.split("|")[0]
        dia = date.split(" ")[1]
        mes = date.split(" ")[2]
        mes = format_mes(mes)
        año = date.split(" ")[4]
        date = año+"-"+mes+"-"+dia
        return date



def format_date(date):
        return(date.split("T")[0])
def webElEpicentro():
        session = HTMLSession()

        ## URL "SEED" que escrapear
        URL_SEED = "https://www.elepicentro.cl/nacional/"

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
        headers = {'user-agent':random.choice(USER_AGENT_LIST) }

        response = session.get(URL_SEED,headers=headers)

        ## Analizar ("to parse") el contenido

        xpath_url="//div[@class='standar-articlelist'] //a/@href"

        all_urls = response.html.xpath(xpath_url)
        for i in range(5):
                all_urls.pop()
        xpath_title="//div/h1//text()" #/span
        xpath_date="//div/h6/text()"

        xpath_text="//div[@class='post-content']//p"
        titles=[]
        dates=[]
        texts=[]
        #print(all_urls)

        for i in all_urls:
                URL_SEED_UNITARY = i
                headers = {'user-agent':random.choice(USER_AGENT_LIST) }
                response = session.get(URL_SEED_UNITARY,headers=headers)
                title = response.html.xpath(xpath_title)[0]
                date = response.html.xpath(xpath_date)[0]
                date = format_date_casero(date)

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
        print("\n ---------------------------------------\n ")
        print('Scrapper hecho en elEpicentro.cl correctamente')
        print("\n --------------------------------------- ")
        return all_urls, dates, title, text
webElEpicentro()