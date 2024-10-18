from flask import Flask, jsonify, request
from utils import get_pokemon_type, get_random_pokemon_by_type, get_longest_name_pokemon, get_random_pokemon_with_letters

app = Flask(__name__)

@app.route('/')
def root():
    return "root"

@app.route('/pokemon/<string:name>', methods=['GET'])
def pokemon_type(name):
    pokemon_type = get_pokemon_type(name)
    return jsonify(pokemon_type)

@app.route('/pokemon/random/<string:type>', methods=['GET'])
def random_pokemon(type):
    pokemon = get_random_pokemon_by_type(type)
    return pokemon

if __name__ == '__main__':
    app.run(debug=True)