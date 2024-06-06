import requests
import json
import csv
import os

url = "https://pokeapi.co/api/v2/pokemon"

nombres_pokemones = []
lista_Pokemon = []


#Comentario
while(url):
    respuesta = requests.get(url)
    poke_respuesta_json = json.loads(respuesta.text)
    nombres_pokemones.extend(poke_respuesta_json['results'])
    url = poke_respuesta_json['next']

#Limpio los datos extraidos
for id,pokemon in enumerate (nombres_pokemones, start=1):
    url_Pokemon = pokemon['url']
    respuesta_datos = requests.get(url_Pokemon)
    poke_datos_json = json.loads(respuesta_datos.text)
    
    nombre = poke_datos_json['name']
    url_imagen = poke_datos_json["sprites"]["other"]["official-artwork"]["front_default"]
    peso = poke_datos_json['weight']/10
    altura = poke_datos_json['height']/10
    
    #Anido a la variable tipo los tipos de cada pokemon 
    tipo = ','.join([tipo['type']['name'] for tipo in poke_datos_json['types']])
    habilidades = ','.join([habilidad['ability']['name'] for habilidad in poke_datos_json['abilities']])
    movimiento = ','.join([movimiento['move']['name'] for movimiento in poke_datos_json['moves']])
    
    
    url_descripcion = poke_datos_json['species']['url']
    respuesta_descripcion = requests.get(url_descripcion)
    poke_descripcion_json = json.loads(respuesta_descripcion.text)
    
    cambio_de_valor = lambda valor: "Si" if (valor == True) else "No"
    
    if(poke_descripcion_json['habitat']):
         habitat = poke_descripcion_json['habitat']['name']
    else:
        habitat = ""
        
    es_baby = cambio_de_valor(poke_descripcion_json['is_baby'])
    es_legendario = cambio_de_valor(poke_descripcion_json['is_legendary'])
    es_mitico = cambio_de_valor(poke_descripcion_json['is_mythical'])
    generacion = poke_descripcion_json['generation']['name']
    descripcion = next((i["flavor_text"].replace("\n", " ") for i in poke_descripcion_json["flavor_text_entries"] if i["language"]["name"] == "es"), "")
    
    
    #Creo un diccionario para guardar los datos    
    poke_diccionario = {
        'Id': id,
        'Nombre': nombre,
        'Imagen': url_imagen,
        'Tipo Pokemon': tipo,
        'Peso': peso,
        'Habilidades': habilidades,
        'Movimiento': movimiento,
        'Altura': altura,
        'Habitat': habitat,
        'Es baby': es_baby,
        'Es Legendario': es_legendario,
        'Es Mitico': es_mitico,
        'Generacion': generacion,
        'Descripcion': descripcion
    }
    
    lista_Pokemon.append(poke_diccionario)
    
archivo_csv = 'pokemon_data.csv'

poke_columnas = [
    'Id', 'Nombre', 'Imagen', 'Tipo Pokemon', 'Peso', 'Habilidades', 'Movimiento',
    'Altura', 'Habitat', 'Es baby', 'Es Legendario', 'Es Mitico', 'Generacion', 'Descripcion'
]

with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
    escritor_csv = csv.DictWriter(archivo, fieldnames=poke_columnas)

    escritor_csv.writeheader()

    escritor_csv.writerows(lista_Pokemon)

print(f'Datos guardados en {archivo_csv}')