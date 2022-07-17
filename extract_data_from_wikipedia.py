#Escribir un script Python que permite extraer la popularidad, la profesión y la fecha de nacimiento de una persona a partir de Wikipedia.
import wikipedia
import pageviewapi
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers import pipeline

#Pedir el nombre de la persona
nombre = input("Introduce el nombre de la persona: ")

#Arreglar el nombre, por si fue ingresado en minúsculas
nombre_mayus = str.title(nombre)
wikipedia.set_lang("es")
text = wikipedia.summary(nombre_mayus)

result=pageviewapi.per_article('es.wikipedia', nombre_mayus, '20220701', '20220705',
                        access='all-access', agent='all-agents', granularity='daily')

ES_MODEL_LANGUAGE="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"

tokenizer_es_language = AutoTokenizer.from_pretrained(ES_MODEL_LANGUAGE)
model_es_language = AutoModelForQuestionAnswering.from_pretrained(ES_MODEL_LANGUAGE)

q_a_es = pipeline("question-answering", model=model_es_language, tokenizer=tokenizer_es_language)

#Imprimir la información solicitada por el enunciado
var1 = q_a_es(question="¿Cuál es su profesión?", context=text)
print(var1["answer"])

var1 = q_a_es(question="¿Cuál es su fecha de nacimiento?", context=text)
print(var1["answer"])

for item in result.items():
    for article in item[1]:
        timestamp = article['timestamp']
        views = article['views']
        print(timestamp, views)