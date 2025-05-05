from ByteUtility import ByteUtility
from Database import Database
from Game import Game
from Lookup import Lookup
from Pokemon import Pokemon


class Extractor:
    
    def get_party_from_bytes(game: Game, lang, content: bytes) -> list[Pokemon]:
        # generation program flow
        party: list[Pokemon] = []
        version = game.version_id
        match version:
            # uses big-endian
            case 1 | 2:
                # get player name
                player_name = ""
                for c in ByteUtility.get_bytes(content, 0x2598, 0xB):
                    char = ByteUtility.get_encoded_character(c, version, lang)
                    if (char != "[end]"):
                        player_name += char
                    else:
                        break
                print(f"Name: [{player_name}]")

                # get party summery
                party_bytes = ByteUtility.get_bytes(content, 0x2F2C, 0x194)
                count = ByteUtility.get_int(party_bytes, 0x00, 0x1)

                # get original trainers
                original_trainers = []
                for i in range(count):
                    start_offset = 0xB*i
                    this_trainer_name_btyes = ByteUtility.get_bytes(party_bytes, 0x110+start_offset, 0xB)
                    original_trainers.append(ByteUtility.get_string(this_trainer_name_btyes, version, lang))
                
                # get nicknames
                pokemon_nicknames = [] 
                for i in range(count):
                    start_offset = 0xB*i
                    this_pokemon_nickname_bytes = ByteUtility.get_bytes(party_bytes, 0x152+start_offset, 0xB)
                    pokemon_nicknames.append(ByteUtility.get_string(this_pokemon_nickname_bytes, version, lang))

                # get party pokemon
                for i in range(count):
                    party_slot_id = i
                    print(f"Looking at party slot #{party_slot_id}")
                    start_offset = 0x8+(0x2C*party_slot_id)
                    pokemon_bytes = ByteUtility.get_bytes(party_bytes, start_offset, 0x2C)
                    pokemon = Pokemon(1)

                    # get pokemon name and OT
                    pokemon.nickname = pokemon_nicknames[i]
                    pokemon.trainer_name = original_trainers[i]
                    pokemon.trainer_id = ByteUtility.get_int(pokemon_bytes,0x0C, 0x02)

                    # https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_I)
                    # get species id
                    pokemon.species_id = Lookup.pokemon_gen1_index.get(int.from_bytes(pokemon_bytes[0x00:0x01]), 0)

                    # get level
                    pokemon.level = ByteUtility.get_int(pokemon_bytes, 0x21, 0x01)
                    pokemon.experience_points = ByteUtility.get_int(pokemon_bytes, 0x0E, 0x03)

                    # get moves
                    pokemon.move1 = ByteUtility.get_int(pokemon_bytes, 0x08, 0x01)
                    pokemon.move2 = ByteUtility.get_int(pokemon_bytes, 0x09, 0x01)
                    pokemon.move3 = ByteUtility.get_int(pokemon_bytes, 0x0A, 0x01)
                    pokemon.move4 = ByteUtility.get_int(pokemon_bytes, 0x0B, 0x01)

                    # pp
                    pp1 = bin(ByteUtility.get_int(pokemon_bytes, 0x1D, 1))[2:].zfill(8)
                    pokemon.move1_pp = int(pp1[2:8], 2)
                    pokemon.move1_pp_times = int(pp1[0:2], 2)

                    pp2 = bin(ByteUtility.get_int(pokemon_bytes, 0x1E, 1))[2:].zfill(8)
                    pokemon.move2_pp = int(pp2[2:8], 2)
                    pokemon.move2_pp_times = int(pp2[0:2], 2)

                    pp3 = bin(ByteUtility.get_int(pokemon_bytes, 0x1F, 1))[2:].zfill(8)
                    pokemon.move3_pp = int(pp3[2:8], 2)
                    pokemon.move3_pp_times = int(pp3[0:2], 2)

                    pp4 = bin(ByteUtility.get_int(pokemon_bytes, 0x20, 1))[2:].zfill(8)
                    pokemon.move4_pp = int(pp4[2:8], 2)
                    pokemon.move4_pp_times = int(pp4[0:2], 2)

                    # get stats
                    pokemon.hp_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x11, 0x02)
                    pokemon.attack_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x13, 0x02)
                    pokemon.defense_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x15, 0x02)
                    pokemon.special_attack_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x19, 0x02)
                    pokemon.special_defense_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x19, 0x02)
                    pokemon.speed_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x17, 0x02)

                    pokemon.hp_stat = ByteUtility.get_int(pokemon_bytes, 0x22, 0x02)
                    pokemon.attack_stat = ByteUtility.get_int(pokemon_bytes, 0x24, 0x02)
                    pokemon.defense_stat = ByteUtility.get_int(pokemon_bytes, 0x26, 0x02)
                    pokemon.special_attack_stat = ByteUtility.get_int(pokemon_bytes, 0x2A, 0x02)
                    pokemon.special_defense_stat = ByteUtility.get_int(pokemon_bytes, 0x2A, 0x02)
                    pokemon.speed_stat = ByteUtility.get_int(pokemon_bytes, 0x28, 0x02)

                    bits = bin(ByteUtility.get_int(pokemon_bytes, 0x1B, 0x02))[2:]
                    iv_stats = [bits[i:i+4] for i in range(0, len(bits), 4)]
                    pokemon.attack_iv = int(iv_stats[0], 2)
                    pokemon.defense_iv = int(iv_stats[1], 2)
                    pokemon.speed_iv = int(iv_stats[2], 2)
                    pokemon.special_attack_iv = int(iv_stats[3], 2)
                    pokemon.special_defense_iv = int(iv_stats[3], 2)

                    party.append(pokemon)
                return party
                    
            case 3 | 4:
                # uses big endian
                # get player name
                player_name = ""
                for c in ByteUtility.get_bytes(content, 0x200B, 0xB):
                    char = ByteUtility.get_encoded_character(c, version, lang)
                    if (char != "[end]"):
                        player_name += char
                    else:
                        break
                print(f"Name: [{player_name}]")

                # get party
                party_bytes = []
                if version == 3:
                    party_bytes = ByteUtility.get_bytes(content, 0x288A, 428)
                else:
                    party_bytes = ByteUtility.get_bytes(content, 0x2865, 428)
                count = ByteUtility.get_int(party_bytes, 0x00, 0x1)

                element_size = 48
                for i in range(count):
                    pokemon = Pokemon(2)
                    pokemon.species_id = ByteUtility.get_int(party_bytes, 0x01+i, 0x01)
                    party.append(pokemon)

                # get original trainers
                for i in range(count):
                    start_offset = 1+(6+1)+(6*element_size)+(i*11)
                    this_trainer_name_btyes = ByteUtility.get_bytes(party_bytes, start_offset, 0xB)
                    party[i].trainer_name = ByteUtility.get_string(this_trainer_name_btyes, version, lang)
                
                # get nicknames
                for i in range(count):
                    start_offset = 1+(6+1)+(6*element_size)+(6*11)+(i*11)
                    this_pokemon_nickname_bytes = ByteUtility.get_bytes(party_bytes, start_offset, 0xB)
                    party[i].nickname = ByteUtility.get_string(this_pokemon_nickname_bytes, version, lang)

                # get party pokemon
                for i in range(count):
                    print(f"Looking at party slot #{i+1}")
                    start_offset = 1+(6+1)+(i*element_size)
                    pokemon_bytes = ByteUtility.get_bytes(party_bytes, start_offset, 48)

                    # get pokemon name and OT
                    party[i].trainer_id = ByteUtility.get_int(pokemon_bytes,0x06, 0x02)

                    # https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_II)

                    # get level
                    party[i].level = ByteUtility.get_int(pokemon_bytes, 0x1F, 0x01)
                    party[i].experience_points = ByteUtility.get_int(pokemon_bytes, 0x08, 0x03)

                    # get moves
                    party[i].move1 = ByteUtility.get_int(pokemon_bytes, 0x02, 0x01)
                    party[i].move2 = ByteUtility.get_int(pokemon_bytes, 0x03, 0x01)
                    party[i].move3 = ByteUtility.get_int(pokemon_bytes, 0x04, 0x01)
                    party[i].move4 = ByteUtility.get_int(pokemon_bytes, 0x05, 0x01)

                    # pp
                    pp1 = bin(ByteUtility.get_int(pokemon_bytes, 0x17, 1))[2:].zfill(8)
                    party[i].move1_pp = int(pp1[2:8], 2)
                    party[i].move1_pp_times = int(pp1[0:2], 2)

                    pp2 = bin(ByteUtility.get_int(pokemon_bytes, 0x18, 1))[2:].zfill(8)
                    party[i].move2_pp = int(pp2[2:8], 2)
                    party[i].move2_pp_times = int(pp2[0:2], 2)

                    pp3 = bin(ByteUtility.get_int(pokemon_bytes, 0x19, 1))[2:].zfill(8)
                    party[i].move3_pp = int(pp3[2:8], 2)
                    party[i].move3_pp_times = int(pp3[0:2], 2)

                    pp4 = bin(ByteUtility.get_int(pokemon_bytes, 0x1A, 1))[2:].zfill(8)
                    party[i].move4_pp = int(pp4[2:8], 2)
                    party[i].move4_pp_times = int(pp4[0:2], 2)

                    # get stats
                    party[i].hp_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x0B, 0x02)
                    party[i].attack_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x0D, 0x02)
                    party[i].defense_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x0F, 0x02)
                    party[i].special_attack_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x13, 0x02)
                    party[i].special_defense_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x13, 0x02)
                    party[i].speed_stat_experience = ByteUtility.get_int(pokemon_bytes, 0x11, 0x02)

                    party[i].hp_stat = ByteUtility.get_int(pokemon_bytes, 0x24, 0x02)
                    party[i].attack_stat = ByteUtility.get_int(pokemon_bytes, 0x26, 0x02)
                    party[i].defense_stat = ByteUtility.get_int(pokemon_bytes, 0x28, 0x02)
                    party[i].special_attack_stat = ByteUtility.get_int(pokemon_bytes, 0x2C, 0x02)
                    party[i].special_defense_stat = ByteUtility.get_int(pokemon_bytes, 0x2E, 0x02)
                    party[i].speed_stat = ByteUtility.get_int(pokemon_bytes, 0x2A, 0x02)

                    bits = bin(ByteUtility.get_int(pokemon_bytes, 0x1B, 0x02))[2:]
                    iv_stats = [bits[i:i+4] for i in range(0, len(bits), 4)]
                    party[i].attack_iv = int(iv_stats[0], 2)
                    party[i].defense_iv = int(iv_stats[1], 2)
                    party[i].speed_iv = int(iv_stats[2], 2)
                    party[i].special_attack_iv = int(iv_stats[3], 2)
                    party[i].special_defense_iv = int(iv_stats[3], 2)
                return party

            case 5 | 6 | 7:

                # https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_III)
                # uses little-endian
                saves = (ByteUtility.get_bytes(content, 0x000000, 57344), ByteUtility.get_bytes(content, 0x00e000, 57344))
                save_indices = (ByteUtility.get_int(saves[0], 0x0ffc, 4, True), ByteUtility.get_int(saves[1], 0x0ffc, 4, True))
                save = None
                print(save_indices)
                if save_indices[0] > save_indices[1]:
                    save = saves[0]
                    print("Using save A")
                else:
                    print ("Using save B")
                    save = saves[1]

                sections: dict[int, bytes] = {}
                for i in range(14):
                    section = ByteUtility.get_bytes(save, (0x1000)*i, 0x1000)
                    section_id = ByteUtility.get_int(section, 0x0ff4, 2, True)
                    sections[section_id] = section

                # get player name
                player_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(sections[0],0x0,7), version, lang)
                trainer_id = ByteUtility.get_int(sections[0], 0x000a, 2, True)
                print(f"OT:{player_name}/{trainer_id}")

                # get party
                party_size = ByteUtility.get_int(sections[1], 0x0234, 4, True)
                party_bytes = ByteUtility.get_bytes(sections[1], 0x0238, 600)

                for i in range(party_size):
                    pokemon = Pokemon(3)
                    pokemon_bytes = ByteUtility.get_bytes(party_bytes, 100*i, 100)
                    
                    pokemon.personality_value = ByteUtility.get_int(pokemon_bytes, 0x00, 4, True)
                    pokemon.trainer_id = ByteUtility.get_int(pokemon_bytes, 0x04, 2, True)
                    pokemon.nickname = ByteUtility.get_encoded_string(ByteUtility.get_bytes(pokemon_bytes, 0x08, 10), version, lang)
                    pokemon.language = ByteUtility.get_int(pokemon_bytes, 0x12, 1, True)
                    pokemon.trainer_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(pokemon_bytes, 0x14, 7), version, lang)
                    pokemon.markings = ByteUtility.get_int(pokemon_bytes, 0x1b, 1, True)
                    pokemon.level = ByteUtility.get_int(pokemon_bytes, 0x54, 1, True)
                    pokemon.mail_id = ByteUtility.get_int(pokemon_bytes, 0x55, 1, True)
                    pokemon.hp_stat = ByteUtility.get_int(pokemon_bytes, 0x58, 2, True)
                    pokemon.attack_stat = ByteUtility.get_int(pokemon_bytes, 0x5a, 2, True)
                    pokemon.defense_stat = ByteUtility.get_int(pokemon_bytes, 0x5c, 2, True)
                    pokemon.speed_stat = ByteUtility.get_int(pokemon_bytes, 0x5e, 2, True)
                    pokemon.special_attack_stat = ByteUtility.get_int(pokemon_bytes, 0x60, 2, True)
                    pokemon.special_defense_stat = ByteUtility.get_int(pokemon_bytes, 0x62, 2, True)
                    checksum = ByteUtility.get_int(pokemon_bytes, 0x1c, 2, True)

                    # data substructure
                    print(pokemon.nickname)
                    substructure_bytes_encrypted = ByteUtility.get_bytes(pokemon_bytes, 0x20, 48)
                    order = pokemon.personality_value % 24
                    
                    permutations = [
                        "GAEM","GAME","GEAM","GEMA",
                        "GMAE","GMEA","AGEM","AGME",
                        "AEGM","AEMG","AMEG","EGAM",
                        "EGMA","EAGM","EAMG","EMGA",
                        "EMAG","MGAE","MGEA","MAGE",
                        "MAEG","MEGA","MEAG"
                    ]
                    order_string = permutations[order]
                    print(f"Order:{order}:{order_string}")
                    decryption_key = bytes(a ^ b for a, b in zip(ByteUtility.get_bytes(pokemon_bytes, 0x04, 4), ByteUtility.get_bytes(pokemon_bytes, 0x00, 4)))
                    print(f"Decryption:{ByteUtility.get_int(decryption_key, 0,4)}")
                    substructure_bytes_decrypted = b''
                    for i in range(48):
                        if i % 4 == 0:
                            this_word = ByteUtility.get_bytes(substructure_bytes_encrypted, 0x1*i, 4)
                            decrypted = bytes(a ^ b for a, b in zip(this_word, decryption_key))
                            substructure_bytes_decrypted += decrypted
                    calculated = 0
                    for i in range(48):
                        if i % 2 == 0:
                            calculated += ByteUtility.get_int(substructure_bytes_decrypted, 0x1*i, 2,True)

                    print(f"{checksum & 0xff} ?== {calculated & 0xff}")
                    print(bin(calculated)[2:].zfill(24))
                    print(bin(checksum)[2:].zfill(24))

                    for i, c in enumerate(order_string):
                        offset = i*12
                        print(f"{c}:{bin(ByteUtility.get_int(substructure_bytes_decrypted, offset, 12, True))[2:].zfill(12*8)}")
                        match c:
                            case "G":
                                pokemon.species_id = Lookup.pokemon_gen3_index.get(ByteUtility.get_int(substructure_bytes_decrypted, 0x0+offset, 2, True),0)
                                pokemon.held_item = ByteUtility.get_int(substructure_bytes_decrypted, 0x2+offset, 2, True)
                                pokemon.experience_points = ByteUtility.get_int(substructure_bytes_decrypted, 0x4+offset, 4, True)
                                pokemon.friendship = ByteUtility.get_int(substructure_bytes_decrypted, 0x9+offset, 1, True)

                                pp_bonuses = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x08+offset, 1, True))[2:].zfill(8)
                                pokemon.move1_pp_times = int(pp_bonuses[0:2], 2)
                                pokemon.move2_pp_times = int(pp_bonuses[2:4], 2)
                                pokemon.move3_pp_times = int(pp_bonuses[4:6], 2)
                                pokemon.move4_pp_times = int(pp_bonuses[6:8], 2)
                                continue

                            case "A":
                                pokemon.move1 = ByteUtility.get_int(substructure_bytes_decrypted, 0x0+offset, 2, True)
                                pokemon.move2 = ByteUtility.get_int(substructure_bytes_decrypted, 0x2+offset, 2, True)
                                pokemon.move3 = ByteUtility.get_int(substructure_bytes_decrypted, 0x4+offset, 2, True)
                                pokemon.move4 = ByteUtility.get_int(substructure_bytes_decrypted, 0x6+offset, 2, True)
                                pokemon.move1_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x8+offset, 1, True)
                                pokemon.move2_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x9+offset, 1, True)
                                pokemon.move3_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x10+offset, 1, True)
                                pokemon.move4_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x11+offset, 1, True)
                                continue

                            case "E":
                                pokemon.hp_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x0+offset, 1, True)
                                pokemon.attack_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x1+offset, 1, True)
                                pokemon.defense_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x2+offset, 1, True)
                                pokemon.speed_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x3+offset, 1, True)
                                pokemon.special_attack_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x4+offset, 1, True)
                                pokemon.special_defense_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x5+offset, 1, True)
                                pokemon.coolness = ByteUtility.get_int(substructure_bytes_decrypted, 0x6+offset, 1, True)
                                pokemon.beauty = ByteUtility.get_int(substructure_bytes_decrypted, 0x7+offset, 1, True)
                                pokemon.cuteness = ByteUtility.get_int(substructure_bytes_decrypted, 0x8+offset, 1, True)
                                pokemon.smartness = ByteUtility.get_int(substructure_bytes_decrypted, 0x9+offset, 1, True)
                                pokemon.toughness = ByteUtility.get_int(substructure_bytes_decrypted, 0x10+offset, 1, True)
                                pokemon.feel = ByteUtility.get_int(substructure_bytes_decrypted, 0x11+offset, 1, True)
                                continue

                            case "M":
                                pokerus = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x0+offset, 1, True))[2:].zfill(8)
                                pokemon.pokerus = int(pokerus[4:8], 2)
                                pokemon.pokerus_days_remaining = int(pokerus[0:4], 2)
                                pokemon.met_location = ByteUtility.get_int(substructure_bytes_decrypted, 0x1+offset, 1, True)

                                origins = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x2+offset, 2, True))[2:].zfill(16)
                                pokemon.trainer_gender = int(origins[15], 2)
                                pokemon.pokeball = int(origins[11:14], 2)
                                pokemon.origin_game = int(origins[7:10], 2)
                                pokemon.level_met = int(origins[0:6], 2)

                                iv_egg_ability = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x4+offset, 4, True))[2:].zfill(32)
                                pokemon.hp_iv = int(iv_egg_ability[0:4], 2)
                                pokemon.attack_iv = int(iv_egg_ability[5:9], 2)
                                pokemon.defense_iv = int(iv_egg_ability[10:14], 2)
                                pokemon.speed_iv = int(iv_egg_ability[15:19], 2)
                                pokemon.special_attack_iv = int(iv_egg_ability[20:24], 2)
                                pokemon.special_defense_iv = int(iv_egg_ability[25:29], 2)
                                pokemon.is_egg = int(iv_egg_ability[30], 2)
                                pokemon.ability = int(iv_egg_ability[31], 2)

                                ribbons_obedience = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x8+offset, 4, True))[2:].zfill(32)
                                pokemon.cool_ribbon = int(ribbons_obedience[0:2], 2)
                                pokemon.beauty_ribbon = int(ribbons_obedience[3:5], 2)
                                pokemon.cute_ribbon = int(ribbons_obedience[6:8], 2)
                                pokemon.smart_ribbon = int(ribbons_obedience[9:11], 2)
                                pokemon.tough_ribbon = int(ribbons_obedience[12:14], 2)
                                pokemon.champion_ribbon = int(ribbons_obedience[15], 2)
                                pokemon.winning_ribbon = int(ribbons_obedience[16], 2)
                                pokemon.victory_ribbon = int(ribbons_obedience[17], 2)
                                pokemon.artist_ribbon = int(ribbons_obedience[18], 2)
                                pokemon.effort_ribbon = int(ribbons_obedience[19], 2)
                                pokemon.battle_champion_ribbon = int(ribbons_obedience[20], 2)
                                pokemon.regional_champion_ribbon = int(ribbons_obedience[21], 2)
                                pokemon.national_champion_ribbon = int(ribbons_obedience[22], 2)
                                pokemon.country_ribbon = int(ribbons_obedience[23], 2)
                                pokemon.national_ribbon = int(ribbons_obedience[24], 2)
                                pokemon.earth_ribbon = int(ribbons_obedience[25], 2)
                                pokemon.world_ribbon = int(ribbons_obedience[26], 2)
                                pokemon.obedience = int(ribbons_obedience[31], 2)
                                continue

                            case _:
                                pass

                    party.append(pokemon)
                return party
            case 7:
                print("working with DPPHGSS")
            case 7:
                print("Working with BWB2W2")
            case _:
                print("Unknown option")
