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

@app.route('/pokemon/longest/<string:type>', methods=['GET'])                   #Endpoint - GET - Devuelve el nombre mas largo de un pokemon segun su tipo
def longest_name_pokemon(type):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return myauth                                                              #Return Error Auth
    pokemon = get_longest_name_pokemon_by_type(type)
    return jsonify(pokemon)

@app.route('/pokemon/random/strong/<string:city>', methods=['GET'])             #Endpoint - GET - Devuelve el nombre de un pokemon random segun la ciudad, temperatura y que tenga las letras iam dentro de su nombre
def temperature(city):
    myauth = validate_authentication()                                              #Valido Autenticacion
    if myauth is not None:
        return myauth                                                              #Return Error Auth
    pokemon = get_random_pokemon_with_letters_by_city(city)
    return jsonify(pokemon)
  

@app.route('/pokemon/pokedex/<string:name>', methods=['GET'])                   #Endpoint - GET - Devuelve tipo de pokemon segun su nombre
def pokemon_pokedex(name):
    pokemon_type =  ', '.join(get_pokemon_type(name))
    pokemon_id = str(get_pokemon_id_by_name(name))
    return render_template('index.html', img_id=pokemon_id, text1=name, text2=pokemon_type)
