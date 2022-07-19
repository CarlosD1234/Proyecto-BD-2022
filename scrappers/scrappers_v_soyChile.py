#Escribir varios scripts Python que permiten “escrapear” automáticamente algunas noticias de prensa publicadas en los medios de prensa de la región, conservando en particular el URL, la fecha de publicación, el título, el texto de la noticia.

import random
from requests_html import HTMLSession
import w3lib.html
import html

from zmq import NULL

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
def webSoyChile(n):    #n = cantidad de páginas a scrapear (las primeras n)

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
        xpath_text="//*[@id='seccion']/div/div/div/div[1]"
        
        all_urls = response.html.xpath(xpath_url)
        URL = []
        #Se debe agregar al path del url el https://www.soychile.cl
        URL +=all_urls
        URL = list(map(agregapath,URL))
        URL = arreglaURL(URL)   #Se arregla ya que habían links tipo: ..../valparaiso o .../quillota
        
        # ITERAMOS EN CADA LINK Y ESCRAPEAMOS LA PÁGINA
        titles = []
        dates = []
        texts = []
        for i in URL:
                URL_SEED_UNITARY = i
                headers = {'user-agent':random.choice(USER_AGENT_LIST) }
                response = session.get(URL_SEED_UNITARY,headers=headers)
                title = response.html.xpath(xpath_title)[0]


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
                dates.append(NULL)
                texts.append(text)


        print("\n ---------------------------------------\n ")        
        print('Scrapper hecho en soyChile correctamente')
        print("\n --------------------------------------- ")        
        return URL, dates, title, text
             




webSoyChile(6)