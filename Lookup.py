import json
from Database import Database
from Models.Game import Game
from Models.Item import Item
from Models.Location import Location

class AbilityMapping:
    first: int
    second: int
    hidden: int

    def __init__(self):
        self.first = self.second = self.hidden = 0

    def assign(self, value, slot, is_hidden):
        if is_hidden == 1:
            self.hidden = value
        else:
            if slot == 1:
                self.first = value
            elif slot == 2:
                self.second = value

    def get_abilities(self) -> tuple[int]:
        return (self.first, self.second)


class Lookup:
    games: dict[int, Game]
    pokemon: dict[int, str]
    moves: dict[int, str]
    items: dict[int, Item]
    abilities: dict[int, str]
    ability_mapping: dict[int, AbilityMapping]
    natures: dict[int, str]
    nature_mapping: dict[int, int]
    gender_rates: dict[int, int]
    base_happiness: dict[int, int]
    language: dict[int, str]
    locations: dict[int, Location]
    pokemon_gen1_index = dict[int, int]
    pokemon_gen3_index = dict[int, int]
    pokemon_gen4_index = dict[int, int]

    def initialize():
        Lookup.games = {}
        Lookup.pokemon = {}
        Lookup.moves = {}
        Lookup.items = {}
        Lookup.abilities = {}
        Lookup.ability_mapping = {}
        Lookup.natures = {}
        Lookup.nature_mapping = {}
        Lookup.language = {}
        Lookup.locations = {}
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

        try:
            with open("mappings/item_index_gen2.json", 'r') as file:
                gen2_item_mapping: dict[int, int] = json.load(file, object_hook=keystoint)
                for (key, value) in gen2_item_mapping.items():
                    Lookup.items[value].id_mapping[2] = key
        except:
            pass

        # abilities
        ability_results = Database.run_query_return_rows("SELECT * FROM abilities")
        for (id, name, generation, main) in ability_results:
            Lookup.abilities[id] = name

        ability_mapping_results = Database.run_query_return_rows("""
            SELECT 
                ps.id, 
                pa.ability_id, 
                pa.slot, 
                pa.is_hidden 
            FROM 
                pokemon p 
                LEFT JOIN pokemon_species ps ON p.species_id = ps.id 
                LEFT JOIN pokemon_abilities pa ON p.id=pa.pokemon_id 
            WHERE p.id <= 10000
        """)

        for (species_id, ability_id, slot, is_hidden) in ability_mapping_results:
            if not species_id in Lookup.ability_mapping:
                Lookup.ability_mapping[species_id] = AbilityMapping()
            Lookup.ability_mapping[species_id].assign(ability_id, slot, is_hidden)

        # natures
        nature_results = Database.run_query_return_rows("SELECT id, identifier, game_index FROM natures")
        for (id, name, game_index) in nature_results:
            Lookup.natures[id] = name
            Lookup.nature_mapping[game_index] = id


        location_results = Database.run_query_return_rows("""
            SELECT 
                l.id, l.identifier, lgi.generation_id, lgi.game_index 
            FROM
                locations l 
                LEFT JOIN location_game_indices lgi ON l.id=lgi.location_id 
            WHERE 
                l.region_id IS NOT NULL 
            ORDER BY
                l.id 
        """)

        for (id, name, generation_id, game_index) in location_results:
            if not id in Lookup.locations:
                Lookup.locations[id] = Location(id, name)
            Lookup.locations[id].generation_indicies[generation_id] = game_index

        try:
            with open("mappings/location_index_gen2.json", 'r') as file:
                gen2_location_mapping: dict[int, int] = json.load(file, object_hook=keystoint)
                for (key, value) in gen2_location_mapping.items():
                    Lookup.locations[value].generation_indicies[2] = key
        except:
            pass
            
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


    def get_item_id_by_index(generation, game_index) -> int:
        if game_index == 0:
            return 0
        
        for item in Lookup.items.values():
            if generation in item.id_mapping.keys():
                if item.id_mapping[generation] == game_index:
                    return item.id
        return 0
    

    def get_item_name(id) -> str:
        if id == 0:
            return ""
        else:
            if id in Lookup.items:
                return Lookup.items[id].name
            else:
                return "???"


    def get_species_id_by_index(generation: int, game_index: int) -> int:
        match generation:
            case 1:
                return Lookup.pokemon_gen1_index.get(game_index, 0)
            case 3:
                return Lookup.pokemon_gen3_index.get(game_index, 0)
            case 4:
                return Lookup.pokemon_gen4_index.get(game_index, 0)
            case _:
                return game_index
            

    def get_species_name(id) -> str:
        return Lookup.pokemon.get(id, "???")
    

    def get_gender_threshold(species_id) -> int:
        threshold = {
            0: 0,
            1: 31,
            2: 63,
            4: 127,
            6: 191,
            7: 225,
            8: 254,
            -1: 255
        } # key/8 chance of being female
        gender_rate = Lookup.get_gender_rate(species_id)
        return threshold.get(gender_rate, 255)
    

    def get_gender_rate(species_id):
        return Lookup.gender_rates.get(species_id, -1)
    

    def get_base_happiness(species_id) -> int:
        return Lookup.base_happiness.get(species_id, 0)
    
    
    def get_abilities(species_id) -> tuple[int]:
        return Lookup.ability_mapping[species_id].get_abilities()
    

    def get_ability_name(ability_id) -> str:
        return Lookup.abilities.get(ability_id, "???")
    

    def get_nature_name(nature_id) -> str:
        return Lookup.natures.get(nature_id, "???")
    

    def get_nature_id_by_index(index) -> int:
        return Lookup.nature_mapping.get(index, 0)