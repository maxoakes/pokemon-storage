import os
import sys
from dotenv import load_dotenv
from CharacterEncoding import CharacterEncoding
from Database import Database
from Lookup import Lookup
from Pokemon import Pokemon

def main():

    VALID_GEN = (1,2,3,4,5)
    VALID_LANG = ("en", "jp", "fr", "de", "es", "it")

    # get generation and language from command line
    mode = None
    lang = "en"
    if len(sys.argv) > 1:
        try:
            mode = int(sys.argv[1])
            if not mode in VALID_GEN:
                raise Exception
        except:
            mode = None
    if len(sys.argv) > 2:
        if sys.argv[2] in VALID_LANG:
            lang = sys.argv[2]

    # get the generation if it was not specified
    if not mode:
        print(
            "Select one of the following modes:",
            "\t1 = Extract Pokemon from North America B/R/Y versions",
            "\t2 = Extract Pokemon from North America G/S/C versions",
            "\t3 = Initialize VBA-M trade with North America R/S/E/FR/LG versions",
            "\t4 = Intialize trade with D/P/P/HG/SS versions",
            "\t5 = Initialize trade with B/W/B2/W2 versions", 
        sep=os.linesep)

        # parse selected generation
        while mode == None:
            try:
                mode = int(input("Selection: "))
                if not mode in VALID_GEN:
                    raise Exception
            except:
                print("Not a valid selection")
                mode = None
    
    # initialize reference database
    load_dotenv(override=True)
    db_config = {
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASS"),
        "host": os.getenv("MYSQL_HOST"),
        "database": os.getenv("MYSQL_DB"),
        "raise_on_warnings": True
    }
    Database.initialize(True, db_config, 1)
    Lookup.initialize()

    # generation program flow
    match mode:
        case 1:
            print("Working with BRY")
            filepath = input("filepath: ")
            content = None
            with open(filepath, 'rb') as f:
                content = f.read()

            # get player name
            player_name = ""
            for c in content[0x2598:0x2598+0xB]:
                char = get_character_by_byte(c, mode, lang)
                if (char != "[end]"):
                    player_name += char
                else:
                    break
            print(f"Name: [{player_name}]")

            # get party summery
            party_bytes = content[0x2F2C:0x2F2C+0x194]
            count = int.from_bytes(party_bytes[0x00:0x1])

            # get original trainers
            original_trainers = []
            for i in range(count):
                start_offset = 0xB*i
                original_trainers.append(get_string_from_bytes(party_bytes[0x110+start_offset:0x110+start_offset+0xB], mode, lang))
            
            # get nicknames
            pokemon_nicknames = [] 
            for i in range(count):
                start_offset = 0xB*i
                pokemon_nicknames.append(get_string_from_bytes(party_bytes[0x152+start_offset:0x152+start_offset+0xB], mode, lang))

            # get party pokemon
            party: list[Pokemon] = []
            for i in range(count):
                party_slot_id = i
                print(f"Looking at party slot #{party_slot_id}")
                start_offset = 0x8+(0x2C*party_slot_id)
                pokemon_bytes = party_bytes[start_offset:start_offset+0x2C]
                pokemon = Pokemon(1)

                # get pokemon name and OT
                pokemon.nickname = pokemon_nicknames[i]
                pokemon.trainer_name = original_trainers[i]
                pokemon.trainer_id = int.from_bytes(pokemon_bytes[0x0C:0x0C+0x02])

                # https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_I)
                # get species id
                id_number = int.from_bytes(pokemon_bytes[0x00:0x01])
                species_results = Database.run_query_return_rows("SELECT ps.id, pgi.pokemon_index, ps.identifier FROM pokemon_species ps LEFT JOIN pokemon_generation_1_indicies pgi ON ps.id=pgi.pokemon_id WHERE pgi.pokemon_index=(%s)", (id_number,))
                if len(species_results) > 0:
                    result = species_results[0]
                    pokemon.species_id = result[0]
                else:
                    print(f"Invalid ID: {id_number}")
                    continue

                # get level
                pokemon.level = int.from_bytes(pokemon_bytes[0x21:0x21+0x01])
                pokemon.experience_points = int.from_bytes(pokemon_bytes[0x0E:0x0E+0x03])

                # get moves
                pokemon.move1 = int.from_bytes(pokemon_bytes[0x08:0x08+0x01])
                pokemon.move2 = int.from_bytes(pokemon_bytes[0x09:0x09+0x01])
                pokemon.move3 = int.from_bytes(pokemon_bytes[0x0A:0x0A+0x01])
                pokemon.move4 = int.from_bytes(pokemon_bytes[0x0B:0x0B+0x01])
                pokemon.move1_pp = pokemon_bytes[0x1D:0x1D+0x01]
                pokemon.move2_pp = pokemon_bytes[0x1E:0x1E+0x01]
                pokemon.move3_pp = pokemon_bytes[0x1F:0x1F+0x01]
                pokemon.move4_pp = pokemon_bytes[0x20:0x20+0x01]

                # get stats
                pokemon.hp_stat_experience = int.from_bytes(pokemon_bytes[0x11:0x11+0x02])
                pokemon.attack_stat_experience = int.from_bytes(pokemon_bytes[0x13:0x13+0x02])
                pokemon.defense_stat_experience = int.from_bytes(pokemon_bytes[0x15:0x15+0x02])
                pokemon.special_attack_stat_experience = int.from_bytes(pokemon_bytes[0x19:0x19+0x02])
                pokemon.special_defense_stat_experience = int.from_bytes(pokemon_bytes[0x19:0x19+0x02])
                pokemon.speed_stat_experience = int.from_bytes(pokemon_bytes[0x17:0x17+0x02])

                pokemon.hp_stat = int.from_bytes(pokemon_bytes[0x22:0x22+0x02])
                pokemon.attack_stat = int.from_bytes(pokemon_bytes[0x24:0x24+0x02])
                pokemon.defense_stat = int.from_bytes(pokemon_bytes[0x26:0x26+0x02])
                pokemon.special_attack_stat = int.from_bytes(pokemon_bytes[0x2A:0x2A+0x02])
                pokemon.special_defense_stat = int.from_bytes(pokemon_bytes[0x2A:0x2A+0x02])
                pokemon.speed_stat = int.from_bytes(pokemon_bytes[0x28:0x28+0x02])

                bits = bin(int.from_bytes(pokemon_bytes[0x1B:0x1B+0x02]))[2:]
                iv_stats = [bits[i:i+4] for i in range(0, len(bits), 4)]
                pokemon.attack_iv = int(iv_stats[0], 2)
                pokemon.defense_iv = int(iv_stats[1], 2)
                pokemon.speed_iv = int(iv_stats[2], 2)
                pokemon.special_attack_iv = int(iv_stats[3], 2)
                pokemon.special_defense_iv = int(iv_stats[3], 2)

                party.append(pokemon)
                pokemon.console_print()
                
        case 2:
            print("Working with GSC")
        case 3:
            print("Working with RSEFRLG")
        case 4:
            print("working with DPPHGSS")
        case 5:
            print("Working with BWB2W2")
        case _:
            print("Unknown option")


def get_character_by_byte(character, generation: int, lang="en"):  
    match generation:
        case 1:
            match lang:
                case "en":
                    return CharacterEncoding.en_us_gen1.get(character, "?")
                case _:
                    pass
        case 2:
            match lang:
                case "en":
                    pass
                case _:
                        pass
        case 3:
            match lang:
                case "en":
                    pass
                case _:
                        pass
        case 4:
            match lang:
                case "en":
                    pass
                case _:
                        pass
        case 5: 
            match lang:
                case "en":
                    pass
                case _:
                        pass
        case _:
            match lang:
                case "en":
                    pass
                case _:
                        pass
    return "?"
       

def get_string_from_bytes(bytes: str, mode: int, lang: str):
    output = ""
    for c in bytes:
        char = get_character_by_byte(c, mode, lang)
        if (char != "[end]"):
            output += char
        else:
            break
    return output


if __name__ == "__main__":
    main()

