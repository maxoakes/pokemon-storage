from Database import Database

class Lookup:
    pokemon = {}
    moves = {}

    def initialize():
        move_results = Database.run_query_return_rows("SELECT id, identifier, generation_id FROM moves")
        for (id, name, gen) in move_results:
            Lookup.moves[id] = name
        
        pokemon_results = Database.run_query_return_rows("SELECT id, identifier, generation_id FROM pokemon_species")
        for (id, name, gen) in pokemon_results:
            Lookup.pokemon[id] = name