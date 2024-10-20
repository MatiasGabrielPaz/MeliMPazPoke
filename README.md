main.py

//Este endpoint GET devuelve un string indicando el tipo del pokemon que es ingresado
Valores de ingreso: name (string) --> Nombre del pokemon
Valores de resultado: pokemon_type (string) --> Tipo del pokemon
Posibles excepciones: myauth (string) --> Mensaje de error por validacion de usuario y contrasenia
                      pokemon_type --> Mensaje de error por nombre de pokemon ingresado incorrecto


@app.route('/pokemon/<string:name>', methods=['GET'])                           #Endpoint - GET - Devuelve tipo de pokemon segun su nombre
def pokemon_type(name):                                                             #
    myauth = validate_authentication()              #Valido Autenticacion
    if myauth is not None:
        return myauth                             #Return Error Auth
    pokemon_type = get_pokemon_type(name)
    return pokemon_type

//Este endpoint GET devuelve un string indicando el nombre del pokemon random seleccionado en base a un tipo especifico ingresado
Valores de ingreso: type (string) --> Tipo del pokemon
Valores de resultado: pokemon (string) --> Nombre del pokemon
Posibles excepciones: myauth (string) --> Mensaje de error por validacion de usuario y contrasenia
                      pokemon --> Mensaje de error por tipo ingresado incorrecto    

@app.route('/pokemon/random/<string:type>', methods=['GET'])                    #Endpoint - GET - Devuelve el nombre de un pokemon random segun su tipo
def random_pokemon(type):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return myauth                                                              #Return Error Auth
    pokemon = get_random_pokemon_by_type(type)
    return pokemon


//Este endpoint GET devuelve un string indicando el nombre del pokemon que tenga la mayor cantidad de caracteres segun el tipo especifico ingresado
Valores de ingreso: type (string) --> Tipo del pokemon
Valores de resultado: pokemon (string) --> Nombre del pokemon
Posibles excepciones: myauth (string) --> Mensaje de error por validacion de usuario y contrasenia
                      pokemon --> Mensaje de error por tipo ingresado incorrecto    


@app.route('/pokemon/longest/<string:type>', methods=['GET'])                   #Endpoint - GET - Devuelve el nombre mas largo de un pokemon segun su tipo
def longest_name_pokemon(type):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return myauth                                                              #Return Error Auth
    pokemon = get_longest_name_pokemon_by_type(type)
    return jsonify(pokemon)

//Este endpoint GET devuelve un string indicando el nombre del pokemon random que contenga alguna de las letras ‘I’,’A’,’M’ en su nombre y que sea del tipo específico más fuerte en base al clima actual de la ciudad ingresada
Valores de ingreso: city (string) --> Nombre de la ciudad
Valores de resultado: pokemon (string) --> Nombre del pokemon
Posibles excepciones: myauth (string) --> Mensaje de error por validacion de usuario y contrasenia
                      pokemon --> Mensaje de error por ciudad ingresada incorrecta

@app.route('/pokemon/random/strong/<string:city>', methods=['GET'])             #Endpoint - GET - Devuelve el nombre de un pokemon random segun la ciudad, temperatura y que tenga las letras iam dentro de su nombre
def temperature(city):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return myauth                                                              #Return Error Auth
    pokemon = get_random_pokemon_with_letters_by_city(city)
    return jsonify(pokemon)
  
//Este endpoint GET devuelve un html que contiene un svg de un pokedex mostrando un png del pokemon ingresado, su nombre y su tipo.

Valores de ingreso: name (string) --> Nombre del pokemon
Valores de resultado: name (string) --> Nombre del pokemon
                      pokemon_type (string) --> Tipos del pokemon
                      index.html --> html que contiene el svg
Posibles excepciones: pokemon_type --> Mensaje de error por nombre de pokemon ingresado incorrecto


@app.route('/pokemon/pokedex/<string:name>', methods=['GET'])                   #Endpoint - GET - Devuelve tipo de pokemon segun su nombre
def pokemon_pokedex(name):
    pokemon_type =  ', '.join(get_pokemon_type(name))
    pokemon_id = str(get_pokemon_id_by_name(name))
    return render_template('index.html', img_id=pokemon_id, text1=name, text2=pokemon_type)

-----------------------------------------------------------------------------------
utils.py



import requests                                     #Que pasa si hay mas de 1 type? Chequear ......get_pokemon_type. RESUELTO
import random                                       #Si hay 2 pokemons con la misma cantidad de letras trae el primero que encuentre.......get_longest_name_pokemon_by_type
from utils import *
import json
from flask import Flask, jsonify, request, render_template
from utils import *
import json
import urllib.request
import hashlib
import os
from werkzeug.security import check_password_hash


POKE_API = "https://pokeapi.co/api/v2"

//Esta funcion

Valores de ingreso: name (string) --> Nombre del pokemon
Valores de resultado: name (string) --> Nombre del pokemon
                      pokemon_type (string) --> Tipos del pokemon
                      index.html --> html que contiene el svg
Posibles excepciones: pokemon_type --> Mensaje de error por nombre de pokemon ingresado incorrecto

def get_pokemon_type(name):                                                     #Function - Muestra el tipo del pokemon segun su nombre
    response = requests.get(f"{POKE_API}/pokemon/{name.lower()}")
    if response.status_code == 200:
        tipos = []
        for p in response.json()['types']:
            tipos.append(p['type']['name'])   
        return tipos         
    return get_error_message(1)                                                 #Error [1] - El pokemon ingresado no existe en la base de datos

def get_random_pokemon_by_type(pokemon_type_wanted):                            #Function - Devuelve el nombre de un pokemon random segun su tipo
    response = requests.get(f"{POKE_API}/pokemon?limit=50")  
    if response.status_code == 200:

        pokemons = []                                                                   # Inicializamos lista vacía
    
        for p in response.json()['results']:                                            # Iteramos sobre cada Pokémon
            pokemon_type = get_pokemon_type(p['name'])                                  # Obtenemos el tipo del Pokémon actual

            for y in pokemon_type:
                if y == pokemon_type_wanted:                                            # Verificamos si el tipo coincide con el tipo deseado  
                    pokemons.append(p['name'])                                          # Si coincide, añadimos el nombre a la lista
                                            
        if pokemons:                                                                    # Si la lista no está vacía, elegimos un Pokémon al azar
            random_pokemon = random.choice(pokemons)
        else:                                                                           # Si la lista está vacía, asignamos None
            return get_error_message(3)                                         #Error [3] - No se encontraron pokemons con de ese tipo
        return random_pokemon
    return get_error_message(2)                                                 #Error [2] - El tipo ingresado no existe en la base de datos

def get_longest_name_pokemon_by_type(pokemon_type_wanted):                      #Function - Devuelve el nombre mas largo que encuentre de la lista de pokemon segun su tipo
    response = requests.get(f"{POKE_API}/pokemon?limit=50")  
    if response.status_code == 200:

        pokemons = []                                                                   # Inicializamos lista vacía
    
        for p in response.json()['results']:                                            # Iteramos sobre cada Pokémon
            pokemon_type = get_pokemon_type(p['name'])                                  # Obtenemos el tipo del Pokémon actual
            for y in pokemon_type:                                                      # Iteramos aca por si el pokemon tiene mas de 1 tipo
                if y == pokemon_type_wanted:                                            # Verificamos si el tipo coincide con el tipo deseado  
                    pokemons.append(p['name'])                                          # Si coincide, añadimos el nombre a la lista
        if pokemons:                                                                    # Si la lista no está vacía, obtenemos el Pokémon con el nombre más largo
            longest_pokemon = max(pokemons, key=len)
        else:                                                                           # Si la lista está vacía, asignamos None
            return get_error_message(3)                                         #Error [3] - No se encontraron pokemons para clasificar
        return longest_pokemon
    return get_error_message(2)                                                 #Error [2] - El tipo ingresado no existe en la base de datos

def get_random_pokemon_with_letters_by_city(city):                              #Function - Devuelve el nombre de pokemon random que contenga IAM en el nombre y sea del tipo mas fuerte en base al clima de la ciudad indicada
    city_temp = get_temperature_by_city(city)                                           #Devuelve la temperatura de la ciudad indicada                                           
    if city_temp == None:
        return get_error_message(9)                                             #Error [9] - La ciudad ingresada no puede ser encontrada en la base de datos
    pokemon_type_required = get_strongest_type_by_temp(city_temp)                       #Devuelve el tipo de pokemon mas fuerte segun la temperatura de la ciudad
    response = requests.get(f"{POKE_API}/pokemon?limit=50")
    if response.status_code == 200:
        results = response.json()['results']                                            #Traemos la lista entera de pokemons
        
        pokemons = []                                                                   #Lista que guarda el tipo de pokemon que necesito
        for p in results:
            pokemon_name = p['name']
            pokemon_type = get_pokemon_type(pokemon_name)
            
            for y in pokemon_type:                                                      # Iteramos aca por si el pokemon tiene mas de 1 tipo
                if y == pokemon_type_required:                                          # Verificamos si el tipo coincide con el tipo deseado  
                    pokemons.append(pokemon_name)                                       # Si coincide, añadimos el nombre a la lista

        filtered_pokemons = []                                                          #Lista que guarda los pokemon que tienen las letras
        
        for p in pokemons:
            contains_letter = any(letter in p for letter in 'iamIAM')
            
            if contains_letter:
                filtered_pokemons.append(p)
                                      
        if filtered_pokemons:                                       
            return random.choice(filtered_pokemons)
        else:
            return get_error_message(7)                                         #Error [7] - No se encontraron pokemons en la lista
    return get_error_message(3)                                                 #Error [8] - Hubo un problema en el procesamiento de la ciudad ingresada


def get_pokemon_id_by_name(name):                                               #Function - Devuelve el id del pokemon a partir de su nombre
    response = requests.get(f"{POKE_API}/pokemon/{name.lower()}")
    if response.status_code == 200:
        return response.json()['id']              
    return get_error_message(1)                                                 #Error [1] - Error 500 - El pokemon ingresado no existe en la base de datos


def get_error_message(error_id):                                                #Function - Diccionario de errores
    errors_descriptions = {
        1: "Error - El pokemon ingresado no existe en la base de datos",
        2: "Error - El tipo ingresado no existe en la base de datos",
        3: "Error - No se encontraron pokemons con de ese tipo",
        4: "Error - Autenticacion no valida",
        5: "Error - Por favor, ingrese la contrasenia para acceder",
        6: "Error - Por favor, ingrese el usuario para acceder",
        7: "Error - No se encontraron pokemons en la lista",
        8: "Error - Hubo un problema en el procesamiento de la ciudad ingresada",
        9: "Error - La ciudad ingresada no puede ser encontrada en la base de datos"
    }
    
    if error_id in errors_descriptions:
        return errors_descriptions[error_id]
    return "Error - El error no se puede visualizar correctamente"



def get_temperature_by_city(city):                                              #Function - Devuelve la temperatura a partir de la ciudad
    
    lat, long = get_coords_by_city(city)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true" # URL de la API de Open-Meteo para obtener el clima actual
    
    try:
        with urllib.request.urlopen(url) as response:                                                           
            data = response.read()
            weather_data = json.loads(data)

        temperature = weather_data['current_weather']['temperature']                # Extraemos la temperatura actual
        
        return temperature
    except:
        return None

    

def get_coords_by_city(city):                                                   #Function - Devuelve las coordenadas de la ciudad a partir del nombre de la ciudad

    city = city.replace(" ","%20")
    url = f"https://nominatim.openstreetmap.org/search?q={city.lower().strip()}&format=json&limit=1"

    with urllib.request.urlopen(url) as response:                                                           
        data = response.read()
        location_data = json.loads(data)

    if location_data:
        latitude = location_data[0]['lat']
        longitude = location_data[0]['lon']
        return latitude, longitude
    else:
        return None, None

def get_strongest_type_by_temp(temperature):                                    #Function - Devuelve el tipo mas fuerte en base a la temperatura
    if temperature >= 30:
        return "fire"
    elif 20 <= temperature < 30:
        return "ground"
    elif 10 <= temperature < 20:
        return "normal"
    elif 0 <= temperature < 10:
        return "water"
    else:
        return "ice"


def verify_password(hash_to_validate):                                          #Function - Verifica la password del usuario, devuelve True si esta OK, false si falla
    with open(r"C:\Users\matyy\Desktop\Pokemon MELI\credentials.json") as file:
        data = json.load(file)
        if hash_to_validate is None:
            return None
        else:
            return check_password_hash(data['users'][0]['password_hash'], hash_to_validate)

def verify_user(hash_to_validate):                                              #Function - Verifica el user del usuario, devuelve True si esta OK, false si falla
    with open(r"C:\Users\matyy\Desktop\Pokemon MELI\credentials.json") as file:
        data = json.load(file)
        if hash_to_validate is None:
            return None
        else:
            return check_password_hash(data['users'][0]['username'], hash_to_validate)
        

def validate_authentication():                                                  #Function - valida el usuario y password.
   
    auth = request.authorization
    if auth is None or 'password' not in auth or not auth['password']:          
        return get_error_message(5) 
    if auth is None or 'username' not in auth or not auth['username']:
        return get_error_message(6) 
    if not verify_password(auth.password) or not verify_user(auth.username):
        return get_error_message(4) 
    else:
        return None
