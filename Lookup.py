import json
from Database import Database
from Game import Game

class Lookup:
    games: dict[int, Game]
    pokemon: dict[int, str]
    moves: dict[int, str]
    pokemon_gen1_index = dict[int, int]
    pokemon_gen3_index = dict[int, int]

    def initialize():
        Lookup.games = {}
        Lookup.pokemon = {}
        Lookup.moves = {}
        Lookup.pokemon_gen1_index = {}
        Lookup.pokemon_gen3_index = {}

        def keystoint(x):
            return {int(k): v for k, v in x.items()}

        try:
            with open("mappings/pokemon_index_gen1.json", 'r') as file:
                Lookup.pokemon_gen1_index = json.load(file, object_hook=keystoint)
        except:
            pass

        try:
            with open("mappings/pokemon_index_gen3.json", 'r') as file:
                Lookup.pokemon_gen3_index = json.load(file, object_hook=keystoint)
        except:
            pass
        
        game_results = Database.run_query_return_rows("""
            SELECT 
                v.id,
                v.version_group_id,
                vg.generation_id,
                vn.name
            FROM
                versions v 
                LEFT JOIN version_groups vg ON vg.id = v.version_group_id 
                LEFT JOIN version_names vn ON v.id = vn.version_id 
            WHERE 
                vn.local_language_id = 9
            ORDER BY vg.`order` 
        """)
        for (id, version, gen, name) in game_results:
            Lookup.games[id] = Game(id, name, version, gen)

        move_results = Database.run_query_return_rows("SELECT id, identifier, generation_id FROM moves")
        for (id, name, gen) in move_results:
            Lookup.moves[id] = name
        
        pokemon_results = Database.run_query_return_rows("SELECT id, identifier FROM pokemon_forms")
        for (id, name) in pokemon_results:
            Lookup.pokemon[id] = name