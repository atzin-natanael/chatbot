import random
import re
import bs4 as bs
import requests
from tqdm import tqdm
import pandas as pd

resp = requests.get('https://horario-siiau.netlify.app/') # "get" request to read data without making a change
resp = resp.text                       # fetch the HTML data
soup = bs.BeautifulSoup(resp, 'lxml')  # convert to BeautifulSoup-type object to work with HTML efficiently
table = soup.find('table')
Nrc = []
Clave = []
Materia = []
Seccion = []
Creditos = []
Cupos = []
Disponibles = []
Hora = []
Dias = []
Edificio = []
Aula = []
Profesor = []

for row in tqdm(table.findAll('tr')[1:]):
    TNrc = row.findAll('td')[0].text
    TClave = row.findAll('td')[1].text
    TMateria = row.findAll('td')[2].text
    TSeccion = row.findAll('td')[3].text
    TCreditos = row.findAll('td')[4].text
    TCupos = row.findAll('td')[5].text
    TDisponibles = row.findAll('td')[6].text
    THora = row.findAll('td')[7].text
    TDias = row.findAll('td')[8].text
    TEdificio = row.findAll('td')[9].text
    TAula = row.findAll('td')[10].text
    TProfesor = row.findAll('td')[11].text
    Nrc.append(TNrc)
    Clave.append(TClave)
    Materia.append(TMateria)
    Seccion.append(TSeccion)
    Creditos.append(TCreditos)
    Cupos.append(TCupos)
    Disponibles.append(TDisponibles)
    Hora.append(THora)
    Dias.append(TDias)
    Edificio.append(TEdificio)
    Aula.append(TAula)
    Profesor.append(TProfesor)

list(zip(Nrc, Clave, Materia, Seccion, Creditos, Cupos, Disponibles, Hora, Dias, Edificio, Aula, Profesor)) #zipped list
unzip_file = [{'Nrc':Nrc,'Clave':Clave,'Materia':Materia,'Seccion':Seccion,'Creditos':Creditos,'Cupos':Cupos, 'Disponibles':Disponibles,'Hora':Hora,'Dias':Dias, 'Edificio':Edificio,'Aula':Aula,'Profesor':Profesor}for Nrc, Clave, Materia, Seccion, Creditos, Cupos, Disponibles, Hora, Dias, Edificio, Aula, Profesor in zip(Nrc, Clave, Materia, Seccion, Creditos, Cupos, Disponibles, Hora, Dias, Edificio, Aula, Profesor)] #unzip the list
df = pd.DataFrame(unzip_file) #create the pandas dataframe
horario = df.to_numpy()
ClaveChida = 'I5890'
cont = 0
for str in Clave:
    cont = cont +1
    if ClaveChida in str:
        print(str)
        print(horario[cont-1])

def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

def message_probability(user_message, recognized_words, single_response= False, required_word =[]):
    message_certainty = 0
    has_required_words = True
    for word in user_message:
        if word in recognized_words:
            message_certainty +=1

    percentage= float(message_certainty) / float(len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words= False
            break
    if has_required_words or single_response:
        return int(percentage*100)
    else:
        return 0
def check_all_messages(message):
    highest_prob = {}

    def response(bot_response, list_of_words, single_response = False, required_words  =[]):
            nonlocal highest_prob
            highest_prob[bot_response]= message_probability(message,list_of_words, single_response, required_words)
    response('Hola', ['hola','saludos','buenas'], single_response = True)
    response('Estoy bien y tu?',['como', 'estas', 'vas', 'va', 'sientes'], required_words=['como'])
    response('Vale, en que te puedo ayuda?', ['bien', 'mal', 'excelente'], single_response = True)
    response('estamos ubicados en la calle 23',['donde', 'ubicados', 'direccion', 'ubicacion'], single_response = True)
    response( 'Al 100 como siempre', ['gracias', 'te lo agradezco','thanks','chido'], single_response= True)
    response('Claro, en que te puedo ayudar?', ['ayuda'], required_words=['ayuda'])
    response('Claro, en que materia te puedo ayudar?',['ocupo','necesito', 'ayuda','con','mi','horario','de','universidad','cucei'], required_words=['horario'])

    best_match = max(highest_prob, key = highest_prob.get)
    print(highest_prob)

    return unknow() if highest_prob[best_match]< 1 else best_match
def unknow():
    response = ['Puedes decirlo de nuevo?', 'No estoy seguro de lo que quieres', 'Buscalo en google, a ver que tal'][random.randrange(3)]
    return response
while True:
    print("Bot: " + get_response(input('You: ')))