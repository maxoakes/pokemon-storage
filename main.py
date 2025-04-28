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
            "\t1 = Extract Pokemon from North America Blue/Red versions",
            "\t2 = Extract Pokemon from North America Yellow version"
            "\t3 = Extract Pokemon from North America Gold/Silver versions",
            "\t4 = Extract Pokemon from North America Crystal version"
            "\t5 = Initialize VBA-M trade with North America Ruby/Sapphire versions",
            "\t6 = Initialize VBA-M trade with North America Emerald versions",
            "\t7 = Initialize VBA-M trade with North America Firered/Leafgreen versions",
            "\t8 = Intialize trade with Diamond/Pearl versions",
            "\t9 = Intialize trade with Platinum version",
            "\t10 = Intialize trade with HeartGold/SoulSilver versions",
            "\t11 = Initialize trade with Black/White versions", 
            "\t14 = Initialize trade with Black2/White2 versions", 
            "\t15 = Initialize trade with X/Y versions", 
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
        case 1 | 2:
            print("Working with BRY")
            filepath = input("filepath: ")
            content = None
            with open(filepath, 'rb') as f:
                content = f.read()

            # get player name
            player_name = ""
            for c in get_bytes(content, 0x2598, 0xB):
                char = get_encoded_character(c, mode, lang)
                if (char != "[end]"):
                    player_name += char
                else:
                    break
            print(f"Name: [{player_name}]")

            # get party summery
            party_bytes = get_bytes(content, 0x2F2C, 0x194)
            count = get_int(party_bytes, 0x00, 0x1)

            # get original trainers
            original_trainers = []
            for i in range(count):
                start_offset = 0xB*i
                this_trainer_name_btyes = get_bytes(party_bytes, 0x110+start_offset, 0xB)
                original_trainers.append(get_string(this_trainer_name_btyes, mode, lang))
            
            # get nicknames
            pokemon_nicknames = [] 
            for i in range(count):
                start_offset = 0xB*i
                this_pokemon_nickname_bytes = get_bytes(party_bytes, 0x152+start_offset, 0xB)
                pokemon_nicknames.append(get_string(this_pokemon_nickname_bytes, mode, lang))

            # get party pokemon
            party: list[Pokemon] = []
            for i in range(count):
                party_slot_id = i
                print(f"Looking at party slot #{party_slot_id}")
                start_offset = 0x8+(0x2C*party_slot_id)
                pokemon_bytes = get_bytes(party_bytes, start_offset, 0x2C)
                pokemon = Pokemon(1)

                # get pokemon name and OT
                pokemon.nickname = pokemon_nicknames[i]
                pokemon.trainer_name = original_trainers[i]
                pokemon.trainer_id = get_int(pokemon_bytes,0x0C, 0x02)

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
                pokemon.level = get_int(pokemon_bytes, 0x21, 0x01)
                pokemon.experience_points = get_int(pokemon_bytes, 0x0E, 0x03)

                # get moves
                pokemon.move1 = get_int(pokemon_bytes, 0x08, 0x01)
                pokemon.move2 = get_int(pokemon_bytes, 0x09, 0x01)
                pokemon.move3 = get_int(pokemon_bytes, 0x0A, 0x01)
                pokemon.move4 = get_int(pokemon_bytes, 0x0B, 0x01)
                pokemon.move1_pp = get_bytes(pokemon_bytes,0x1D, 0x01)
                pokemon.move2_pp = get_bytes(pokemon_bytes,0x1E, 0x01)
                pokemon.move3_pp = get_bytes(pokemon_bytes,0x1F, 0x01)
                pokemon.move4_pp = get_bytes(pokemon_bytes,0x20, 0x01)

                # get stats
                pokemon.hp_stat_experience = get_int(pokemon_bytes, 0x11, 0x02)
                pokemon.attack_stat_experience = get_int(pokemon_bytes, 0x13, 0x02)
                pokemon.defense_stat_experience = get_int(pokemon_bytes, 0x15, 0x02)
                pokemon.special_attack_stat_experience = get_int(pokemon_bytes, 0x19, 0x02)
                pokemon.special_defense_stat_experience = get_int(pokemon_bytes, 0x19, 0x02)
                pokemon.speed_stat_experience = get_int(pokemon_bytes, 0x17, 0x02)

                pokemon.hp_stat = get_int(pokemon_bytes, 0x22, 0x02)
                pokemon.attack_stat = get_int(pokemon_bytes, 0x24, 0x02)
                pokemon.defense_stat = get_int(pokemon_bytes, 0x26, 0x02)
                pokemon.special_attack_stat = get_int(pokemon_bytes, 0x2A, 0x02)
                pokemon.special_defense_stat = get_int(pokemon_bytes, 0x2A, 0x02)
                pokemon.speed_stat = get_int(pokemon_bytes, 0x28, 0x02)

                bits = bin(get_int(pokemon_bytes, 0x1B, 0x02))[2:]
                iv_stats = [bits[i:i+4] for i in range(0, len(bits), 4)]
                pokemon.attack_iv = int(iv_stats[0], 2)
                pokemon.defense_iv = int(iv_stats[1], 2)
                pokemon.speed_iv = int(iv_stats[2], 2)
                pokemon.special_attack_iv = int(iv_stats[3], 2)
                pokemon.special_defense_iv = int(iv_stats[3], 2)

                party.append(pokemon)
                pokemon.console_print()
                
        case 3 | 4:
            print("Working with GSC")
            filepath = input("filepath: ")
            content = None
            with open(filepath, 'rb') as f:
                content = f.read()

            # get player name
            player_name = ""
            for c in get_bytes(content, 0x200B, 0xB):
                char = get_encoded_character(c, mode, lang)
                if (char != "[end]"):
                    player_name += char
                else:
                    break
            print(f"Name: [{player_name}]")

            # get party
            party_bytes = []
            if mode == 3:
                party_bytes = get_bytes(content, 0x288A, 428)
            else:
                party_bytes = get_bytes(content, 0x2865, 428)
            count = get_int(party_bytes, 0x00, 0x1)

            element_size = 48
            party: list[Pokemon] = []
            for i in range(count):
                this_pokemon = Pokemon(mode)
                this_pokemon.species_id = get_int(party_bytes, 0x01+i, 0x01)
                party.append(this_pokemon)

            # get original trainers
            for i in range(count):
                start_offset = 1+(6+1)+(6*element_size)+(i*11)
                this_trainer_name_btyes = get_bytes(party_bytes, start_offset, 0xB)
                party[i].trainer_name = get_string(this_trainer_name_btyes, mode, lang)
            
            # get nicknames
            for i in range(count):
                start_offset = 1+(6+1)+(6*element_size)+(6*11)+(i*11)
                this_pokemon_nickname_bytes = get_bytes(party_bytes, start_offset, 0xB)
                party[i].nickname = get_string(this_pokemon_nickname_bytes, mode, lang)

            # get party pokemon
            for i in range(count):
                print(f"Looking at party slot #{i+1}")
                start_offset = 1+(6+1)+(i*element_size)
                pokemon_bytes = get_bytes(party_bytes, start_offset, 48)

                # get pokemon name and OT
                party[i].trainer_id = get_int(pokemon_bytes,0x06, 0x02)

                # https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_II)

                # get level
                party[i].level = get_int(pokemon_bytes, 0x1F, 0x01)
                party[i].experience_points = get_int(pokemon_bytes, 0x08, 0x03)

                # get moves
                party[i].move1 = get_int(pokemon_bytes, 0x02, 0x01)
                party[i].move2 = get_int(pokemon_bytes, 0x03, 0x01)
                party[i].move3 = get_int(pokemon_bytes, 0x04, 0x01)
                party[i].move4 = get_int(pokemon_bytes, 0x05, 0x01)
                party[i].move1_pp = get_bytes(pokemon_bytes,0x17, 0x01)
                party[i].move2_pp = get_bytes(pokemon_bytes,0x18, 0x01)
                party[i].move3_pp = get_bytes(pokemon_bytes,0x19, 0x01)
                party[i].move4_pp = get_bytes(pokemon_bytes,0x1A, 0x01)

                # get stats
                party[i].hp_stat_experience = get_int(pokemon_bytes, 0x0B, 0x02)
                party[i].attack_stat_experience = get_int(pokemon_bytes, 0x0D, 0x02)
                party[i].defense_stat_experience = get_int(pokemon_bytes, 0x0F, 0x02)
                party[i].special_attack_stat_experience = get_int(pokemon_bytes, 0x13, 0x02)
                party[i].special_defense_stat_experience = get_int(pokemon_bytes, 0x13, 0x02)
                party[i].speed_stat_experience = get_int(pokemon_bytes, 0x11, 0x02)

                party[i].hp_stat = get_int(pokemon_bytes, 0x24, 0x02)
                party[i].attack_stat = get_int(pokemon_bytes, 0x26, 0x02)
                party[i].defense_stat = get_int(pokemon_bytes, 0x28, 0x02)
                party[i].special_attack_stat = get_int(pokemon_bytes, 0x2C, 0x02)
                party[i].special_defense_stat = get_int(pokemon_bytes, 0x2E, 0x02)
                party[i].speed_stat = get_int(pokemon_bytes, 0x2A, 0x02)

                bits = bin(get_int(pokemon_bytes, 0x1B, 0x02))[2:]
                iv_stats = [bits[i:i+4] for i in range(0, len(bits), 4)]
                party[i].attack_iv = int(iv_stats[0], 2)
                party[i].defense_iv = int(iv_stats[1], 2)
                party[i].speed_iv = int(iv_stats[2], 2)
                party[i].special_attack_iv = int(iv_stats[3], 2)
                party[i].special_defense_iv = int(iv_stats[3], 2)

                party.append(party[i])
                party[i].console_print()

        case 3:
            print("Working with RSEFRLG")
        case 4:
            print("working with DPPHGSS")
        case 5:
            print("Working with BWB2W2")
        case _:
            print("Unknown option")
       

def get_string(bytes: str, mode: int, lang: str):
    output = ""
    for c in bytes:
        char = get_encoded_character(c, mode, lang)
        if (char != "[end]"):
            output += char
        else:
            break
    return output


def get_int(bytes, offset, length):
    return int.from_bytes(get_bytes(bytes, offset, length))


def get_bytes(data, offset: int, length: int):
    return data[offset:offset+length]


def get_encoded_character(character, generation: int, lang="en"):  
    match generation:
        case 1 | 2:
            match lang:
                case "en":
                    return CharacterEncoding.en_us_gen1.get(character, "?")
                case _:
                    pass
        case 3 | 4:
            match lang:
                case "en":
                    return CharacterEncoding.en_us_gen2.get(character, "?")
                case _:
                        pass
        case _:
            match lang:
                case "en":
                    pass
                case _:
                        pass
    return "?"


if __name__ == "__main__":
    main()

