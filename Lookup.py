import json
import random
from Database import Database
from Models.Game import Game
from Models.Item import Item
    
class Lookup:
    games: dict[int, Game]
    pokemon: dict[int, str]
    moves: dict[int, str]
    items: dict[int, Item]
    abilities: dict[int, str]
    gender_rates: dict[int, int]
    base_happiness: dict[int, int]
    language: dict[int, str]
    gender: dict[int, str]
    pokemon_gen1_index = dict[int, int]
    pokemon_gen3_index = dict[int, int]
    pokemon_gen4_index = dict[int, int]

    def initialize():
        Lookup.games = {}
        Lookup.pokemon = {}
        Lookup.moves = {}
        Lookup.items = {}
        Lookup.abilities = {}
        Lookup.language = {}
        Lookup.gender = {}
        Lookup.gender_rates = {}
        Lookup.base_happiness = {}
        Lookup.pokemon_gen1_index = {}
        Lookup.pokemon_gen3_index = {}
        Lookup.pokemon_gen4_index = {}

        # pokemon species game index id mappings
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

        pokemon_species_results = Database.run_query_return_rows("SELECT id, generation_id, gender_rate, base_happiness FROM pokemon_species")
        for (id, generation_id, gender, happiness) in pokemon_species_results:
            if generation_id in (1,2,3,4):
                Lookup.pokemon_gen4_index[id] = id
            Lookup.gender_rates[id] = gender
            Lookup.base_happiness[id] = happiness

        # special cases for gen4
        Lookup.pokemon_gen4_index[496] = 386
        Lookup.pokemon_gen4_index[497] = 386
        Lookup.pokemon_gen4_index[498] = 386
        Lookup.pokemon_gen4_index[499] = 413
        Lookup.pokemon_gen4_index[500] = 413
        Lookup.pokemon_gen4_index[501] = 487
        Lookup.pokemon_gen4_index[502] = 492
        Lookup.pokemon_gen4_index[503] = 479
        Lookup.pokemon_gen4_index[504] = 479
        Lookup.pokemon_gen4_index[505] = 479
        Lookup.pokemon_gen4_index[506] = 479
        Lookup.pokemon_gen4_index[507] = 479

        # game ids 
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

        # moves
        move_results = Database.run_query_return_rows("SELECT id, identifier, generation_id FROM moves")
        for (id, name, gen) in move_results:
            Lookup.moves[id] = name
        
        # pokemon
        pokemon_results = Database.run_query_return_rows("SELECT id, identifier FROM pokemon_forms")
        for (id, name) in pokemon_results:
            Lookup.pokemon[id] = name

        # items
        item_results = Database.run_query_return_rows("""
            SELECT 
                i.id, 
                i.identifier, 
                igi.generation_id, 
                igi.game_index 
            FROM items i 
                LEFT JOIN item_game_indices igi ON i.id = igi.item_id 
            ORDER BY igi.generation_id, game_index
        """)

        for (id, identifier, generation, game_index) in item_results:
            if id in Lookup.items:
                Lookup.items[id].id_mapping[generation] = game_index
            else:
                Lookup.items[id] = Item(id, identifier)

        # abilities
        ability_results = Database.run_query_return_rows("SELECT * FROM abilities")
        for (id, name, generation, main) in ability_results:
            Lookup.abilities[id] = name

        # lang
        Lookup.language[0] = ""
        Lookup.language[1] = "JP"
        Lookup.language[2] = "EN"
        Lookup.language[3] = "FR"
        Lookup.language[4] = "IT"
        Lookup.language[5] = "DE"
        Lookup.language[6] = ""
        Lookup.language[7] = "ES"
        Lookup.language[8] = "KR"

        # gender
        Lookup.gender[0] = "M"
        Lookup.gender[1] = "F"
        Lookup.gender[2] = "X"


    def get_item_name_by_id(generation, game_index) -> str:
        if game_index == 0:
            return ""
        
        for item in Lookup.items.values():
            if generation in item.id_mapping.keys():
                if item.id_mapping[generation] == game_index:
                    return item.identifier
        return "?"
    
    def get_random_gender(species_id) -> int:
        rate_id = Lookup.gender_rates.get(species_id, -1)
        if rate_id == -1:
            return 2
        
        if random.random() < (rate_id / 8):
            return 1
        else:
            return 0
        
    def get_random_personality() -> int:
        return random.randint(0, 2**32)