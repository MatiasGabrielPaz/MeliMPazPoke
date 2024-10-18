import requests
import random 

POKE_API = "https://pokeapi.co/api/v2"

def get_pokemon_type(name):
    response = requests.get(f"{POKE_API}/pokemon/{name.lower()}")
    if response.status_code == 200:
        return response.json()['types'][0]['type']['name'] #hacer que me traiga mas types si tiene mas types
    return "lala"

def get_random_pokemon_by_type(pokemon_type_wanted):
    response = requests.get(f"{POKE_API}/pokemon?limit=100")  
    if response.status_code == 200:


        # Inicializamos lista vacía
        pokemons = []
        # Iteramos sobre cada Pokémon 
        for p in response.json()['results']:
            # Obtenemos el tipo del Pokémon actual
            pokemon_type = get_pokemon_type(p['name'])
            
            # Verificamos si el tipo coincide con el tipo deseado
            if pokemon_type == pokemon_type_wanted:
                # Si coincide, añadimos el nombre a la lista
                pokemons.append(p['name'])
    return pokemons
    return None

