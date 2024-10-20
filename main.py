from flask import Flask, jsonify, request, render_template
from utils import *
import json
import urllib.request
import hashlib
import os
from werkzeug.security import check_password_hash

app = Flask(__name__)

@app.route('/')
def root():
    return "root"

@app.route('/pokemon/<string:name>', methods=['GET'])                           #Endpoint - GET - Devuelve tipo de pokemon segun su nombre
def pokemon_type(name):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return "myauth"                                                             #Return Error Auth
    pokemon_type = get_pokemon_type(name)
    return jsonify(pokemon_type)

@app.route('/pokemon/random/<string:type>', methods=['GET'])                    #Endpoint - GET - Devuelve el nombre de un pokemon random segun su tipo
def random_pokemon(type):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return "myauth"                                                             #Return Error Auth
    pokemon = get_random_pokemon_by_type(type)
    return jsonify(pokemon)

@app.route('/pokemon/longest/<string:type>', methods=['GET'])                   #Endpoint - GET - Devuelve el nombre mas largo de un pokemon segun su tipo
def longest_name_pokemon(type):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return "myauth"                                                             #Return Error Auth
    pokemon = get_longest_name_pokemon_by_type(type)
    return jsonify(pokemon)

@app.route('/pokemon/random/strong/<string:city>', methods=['GET'])             #Endpoint - GET - Devuelve el nombre de un pokemon random segun la ciudad, temperatura y que tenga las letras iam dentro de su nombre
def temperature(city):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return "myauth"                                                             #Return Error Auth
    pokemon = get_random_pokemon_with_letters_by_city(city)
    return jsonify(pokemon)
  

@app.route('/pokemon/pokedex/<string:name>', methods=['GET'])                   #Endpoint - GET - Devuelve tipo de pokemon segun su nombre
def pokemon_pokedex(name):
    pokemon_type =  ', '.join(get_pokemon_type(name))
    pokemon_id = str(get_pokemon_id_by_name(name))
    return render_template('index.html', img_id=pokemon_id, text1=name, text2=pokemon_type)

    
if __name__ == '__main__':
    app.run(debug=True) #Cambiar False