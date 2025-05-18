from ByteUtility import ByteUtility
from Models.Enum import Gender
from Models.Game import Game
from Lookup import Lookup
from Models.Pokemon import Pokemon
from Models.Trainer import Trainer

class Extractor:
    
    def get_party_from_bytes(game: Game, lang: str, content: bytes) -> list[Pokemon]:
        # generation program flow
        party: list[Pokemon] = []
        trainer = None
        version = game.version_id
        match version:
            
            case 1 | 2:
                # uses big-endian
                player_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(content, 0x2598, 11), version, lang)
                trainer = Trainer(player_name, 0, ByteUtility.get_int(content, 0x2605, 2), 0)
                print(f"Reading Trainer: {trainer}")

                # get party summery
                party_bytes = ByteUtility.get_bytes(content, 0x2F2C, 0x194)
                count = ByteUtility.get_int(party_bytes, 0x00, 0x1)

                # get party pokemon
                for i in range(count):
                    nickname_bytes = ByteUtility.get_bytes(party_bytes, 0x152+(0xB*i), 0xB)
                    nickname = ByteUtility.get_encoded_string(nickname_bytes, version, lang)

                    ot_name_bytes = ByteUtility.get_bytes(party_bytes, 0x110+(0xB*i), 0xB)
                    ot_name = ByteUtility.get_encoded_string(ot_name_bytes, version, lang)

                    pokemon_bytes = ByteUtility.get_bytes(party_bytes, 0x8+(0x2C*i), 0x2C)

                    pokemon = Pokemon(1)
                    pokemon.load_from_gen1_bytes(pokemon_bytes, version, nickname, ot_name)
                    party.append(pokemon)
                return party
                    
            case 3 | 4:
                # uses big endian
                player_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(content, 0x200B, 11), version, lang)
                trainer = Trainer(player_name, 0, ByteUtility.get_int(content, 0x2009, 2), 0)
                if version == 4 and trainer.public_id % 1 == 1:
                    trainer.gender = Gender.FEMALE

                print(f"Reading Trainer: {trainer}")

                # get party
                party_bytes = []
                if version == 3:
                    party_bytes = ByteUtility.get_bytes(content, 0x288A, 428)
                else:
                    party_bytes = ByteUtility.get_bytes(content, 0x2865, 428)
                count = ByteUtility.get_int(party_bytes, 0x00, 1)

                # get party pokemon
                element_size = 48
                for i in range(count):
                    ot_name_bytes = ByteUtility.get_bytes(party_bytes, 0x8+(6*element_size)+(i*11), 11)
                    ot_name = ByteUtility.get_encoded_string(ot_name_bytes, version, lang)

                    nickname_bytes = ByteUtility.get_bytes(party_bytes, 0x4A+(6*element_size)+(i*11), 11)
                    nickname = ByteUtility.get_encoded_string(nickname_bytes, version, lang)

                    pokemon_bytes = ByteUtility.get_bytes(party_bytes, 0x8+(i*element_size), 48)
                    pokemon = Pokemon(2)
                    pokemon.load_from_gen2_bytes(pokemon_bytes, version, nickname, ot_name)
                    party.append(pokemon)
                return party

            case 5 | 6 | 7:

                # https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_III)
                # uses little-endian
                saves = (ByteUtility.get_bytes(content, 0x000000, 57344), ByteUtility.get_bytes(content, 0x00E000, 57344))
                save_indices = (ByteUtility.get_int(saves[0], 0x0FFC, 4, True), ByteUtility.get_int(saves[1], 0x0FFC, 4, True))
                save = None
                print(save_indices)
                if save_indices[0] > save_indices[1] and save_indices[0] != (2**32)-1:
                    save = saves[0]
                    print("Using save A")
                else:
                    print ("Using save B")
                    save = saves[1]

                sections: dict[int, bytes] = {}
                for i in range(14):
                    section = ByteUtility.get_bytes(save, (0x1000)*i, 0x1000)
                    section_id = ByteUtility.get_int(section, 0x0FF4, 2, True)
                    sections[section_id] = section

                trainer = Trainer(
                    ByteUtility.get_encoded_string(ByteUtility.get_bytes(sections[0],0x0,7), version, lang), 
                    ByteUtility.get_int(sections[0], 0x0008, 1, True), 
                    ByteUtility.get_int(sections[0], 0x000A, 2, True), 
                    ByteUtility.get_int(sections[0], 0x000C, 2, True)
                )

                # get party
                party_size_offset = 0x0234 if version in (5,6) else 0x0034
                party_offset = 0x0238 if version in (5,6) else 0x0038
                party_size = ByteUtility.get_int(sections[1], party_size_offset, 4, True)
                party_bytes = ByteUtility.get_bytes(sections[1], party_offset, 600)

                for i in range(party_size):
                    pokemon = Pokemon(3)
                    pokemon_bytes = ByteUtility.get_bytes(party_bytes, 100*i, 100)
                    pokemon.load_from_gen3_bytes(pokemon_bytes, version, lang)
                    party.append(pokemon)
                return party

            case 8 | 9 | 10:
                # https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_IV)
                # https://projectpokemon.org/home/docs/gen-4/hgss-save-structure-r76/
                save = ByteUtility.get_bytes(content, 0x0, 49407)

                # get player name
                player_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(save,0x68,0x77-0x68), version, lang)
                trainer_id = ByteUtility.get_int(save, 0x078, 2, True)
                
                # get party
                party_size = ByteUtility.get_int(save, 0x9c, 1, True)
                party_bytes = ByteUtility.get_bytes(save, 0xa0, 0x628-0xa0)

                if version == 10:
                    # get player name
                    player_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(save,0x64,16), version, lang)
                    trainer_id = ByteUtility.get_int(save, 0x074, 2, True)

                    # get party
                    party_size = ByteUtility.get_int(save, 0x94, 1, True)
                    party_bytes = ByteUtility.get_bytes(save, 0x98, 236*6)

                print(f"OT:{player_name}/{trainer_id}")
                print(party_size, len(party_bytes))

                for i in range(party_size):
                    pokemon = Pokemon(4)
                    pokemon_bytes = ByteUtility.get_bytes(party_bytes, 236*i, 236)

                    # decryption
                    checksum = ByteUtility.get_int(pokemon_bytes, 0x06, 2, True)
                    substructure_bytes_encrypted = ByteUtility.get_bytes(pokemon_bytes, 0x08, 128)

                    prng = checksum
                    word_size = 2
                    substructure_bytes_decrypted = b''
                    for i in range(64*word_size):
                        if i % word_size == 0:
                            prng = ((0x41C64E6D * prng) + 0x6073) 
                            rand = prng >> 16
                            y = ByteUtility.get_int(substructure_bytes_encrypted, i, word_size, True)
                            unencrypted = (y ^ rand) & 0xffff
                            substructure_bytes_decrypted += unencrypted.to_bytes(word_size, 'little')                    

                    # checksum calculation
                    calculated = 0
                    for i in range(64*word_size):
                        if i % word_size == 0:
                            calculated += ByteUtility.get_int(substructure_bytes_decrypted, i, 2, True)
                    calculated = calculated & 0xffff

                    print(f"Cksm:{bin(checksum)[2:].zfill(16)} = {checksum}")
                    print(f"Calc:{bin(calculated)[2:].zfill(16)} = {calculated}")

                    # block order
                    order = {
                        0:"ABCD", 1:"ABDC", 2:"ACBD", 3:"ACDB",
                        4:"ADBC", 5:"ADCB", 6:"BACD", 7:"BADC",
                        8:"BCAD", 9:"BCDA", 10:"BDAC", 11:"BDCA",
                        12:"CABD", 13:"CADB", 14:"CBAD", 15:"CBDA",
                        16:"CDAB", 17:"CDBA", 18:"DABC", 19:"DACB",
                        20:"DBAC", 21:"DBCA", 22:"DCAB", 23:"DCBA"
                    }

                    inverse = {
                        0:"ABCD", 
                        1:"ABDC", 
                        2:"ACBD", 
                        3:"ADBC",
                        4:"ACDB", 
                        5:"ADCB", 
                        6:"BACD", 
                        7:"BADC",
                        8:"CABD", 
                        9:"DABC", 
                        10:"CADB", 
                        11:"DACB",
                        12:"BCAD", 
                        13:"BDAC", 
                        14:"CBAD", 
                        15:"DBAC",
                        16:"CDAB", 
                        17:"DCAB", 
                        18:"BCDA", 
                        19:"BDCA",
                        20:"CBDA", 
                        21:"DBCA", 
                        22:"CDBA", 
                        23:"DCBA"
                    }
                    
                    pokemon.personality_value = ByteUtility.get_int(pokemon_bytes, 0x00, 4, True)
                    sort_order = ((pokemon.personality_value & 0x3E000) >> 0xD) % 24
                    order_string = order[sort_order]
                    print(f"Order:{sort_order}:{order_string}")
                    
                    block_size = 32
                    for i, c in enumerate(order_string):
                        offset = (i*block_size)-8
                        # print(f"{c}:{bin(ByteUtility.get_int(substructure_bytes_decrypted, offset, block_size, True))[2:].zfill(block_size*8)}")
                        match c:
                            case "A":
                                pokemon.species_id = Lookup.pokemon_gen4_index.get(ByteUtility.get_int(substructure_bytes_decrypted, 0x08+offset, 2, True),0)
                                pokemon.held_item = ByteUtility.get_int(substructure_bytes_decrypted, 0xA+offset, 2, True)
                                pokemon.trainer_id = ByteUtility.get_int(substructure_bytes_decrypted, 0x0C+offset, 2, True)
                                pokemon.trainer_secret_id = ByteUtility.get_int(substructure_bytes_decrypted, 0x0E+offset, 2, True)
                                pokemon.experience_points = ByteUtility.get_int(substructure_bytes_decrypted, 0x10+offset, 4, True)
                                pokemon.friendship = ByteUtility.get_int(substructure_bytes_decrypted, 0x14+offset, 1, True)
                                pokemon.ability = ByteUtility.get_int(substructure_bytes_decrypted, 0x15+offset, 1, True)
                                pokemon.markings = ByteUtility.get_int(substructure_bytes_decrypted, 0x16+offset, 1, True)
                                pokemon.language = ByteUtility.get_int(substructure_bytes_decrypted, 0x17+offset, 1, True)
                                pokemon.hp_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x18+offset, 1, True)
                                pokemon.attack_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x19+offset, 1, True)
                                pokemon.defense_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x1A+offset, 1, True)
                                pokemon.speed_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x1B+offset, 1, True)
                                pokemon.special_attack_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x1C+offset, 1, True)
                                pokemon.special_defense_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x1D+offset, 1, True)
                                pokemon.coolness = ByteUtility.get_int(substructure_bytes_decrypted, 0x1E+offset, 1, True)
                                pokemon.beauty = ByteUtility.get_int(substructure_bytes_decrypted, 0x1F+offset, 1, True)
                                pokemon.cuteness = ByteUtility.get_int(substructure_bytes_decrypted, 0x20+offset, 1, True)
                                pokemon.smartness = ByteUtility.get_int(substructure_bytes_decrypted, 0x21+offset, 1, True)
                                pokemon.toughness = ByteUtility.get_int(substructure_bytes_decrypted, 0x22+offset, 1, True)
                                pokemon.sheen = ByteUtility.get_int(substructure_bytes_decrypted, 0x23+offset, 1, True)
                                pokemon.sinnoh_ribbons_1 = ByteUtility.get_int(substructure_bytes_decrypted, 0x24+offset, 3, True)
                                continue

                            case "B":
                                offset -= 32
                                pokemon.move1 = ByteUtility.get_int(substructure_bytes_decrypted, 0x28+offset, 2, True)
                                pokemon.move2 = ByteUtility.get_int(substructure_bytes_decrypted, 0x2A+offset, 2, True)
                                pokemon.move3 = ByteUtility.get_int(substructure_bytes_decrypted, 0x2C+offset, 2, True)
                                pokemon.move4 = ByteUtility.get_int(substructure_bytes_decrypted, 0x2E+offset, 2, True)
                                pokemon.move1_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x30+offset, 1, True)
                                pokemon.move2_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x31+offset, 1, True)
                                pokemon.move3_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x32+offset, 1, True)
                                pokemon.move4_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x33+offset, 1, True)
                                pokemon.move1_pp_times = ByteUtility.get_int(substructure_bytes_decrypted, 0x34+offset, 1, True)
                                pokemon.move2_pp_times = ByteUtility.get_int(substructure_bytes_decrypted, 0x35+offset, 1, True)
                                pokemon.move3_pp_times = ByteUtility.get_int(substructure_bytes_decrypted, 0x36+offset, 1, True)
                                pokemon.move4_pp_times = ByteUtility.get_int(substructure_bytes_decrypted, 0x37+offset, 1, True)

                                iv_stats = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x38+offset, 0x3B-0x38, True))[2:].zfill(32)
                                pokemon.hp_iv = int(iv_stats[0:4], 2)
                                pokemon.attack_iv = int(iv_stats[5:9], 2)
                                pokemon.defense_iv = int(iv_stats[10:14], 2)
                                pokemon.speed_iv = int(iv_stats[15:19], 2)
                                pokemon.special_attack_iv = int(iv_stats[20:24], 2)
                                pokemon.special_defense_iv = int(iv_stats[25:29], 2)
                                pokemon.is_egg = int(iv_stats[30], 2)
                                pokemon.has_nickname = int(iv_stats[31], 2)

                                hoenn_ribbons = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x3c+offset, 4, True))[2:].zfill(32)
                                pokemon.cool_ribbon = int(hoenn_ribbons[0:2], 2)
                                pokemon.beauty_ribbon = int(hoenn_ribbons[3:5], 2)
                                pokemon.cute_ribbon = int(hoenn_ribbons[6:8], 2)
                                pokemon.smart_ribbon = int(hoenn_ribbons[9:11], 2)
                                pokemon.tough_ribbon = int(hoenn_ribbons[12:14], 2)
                                pokemon.champion_ribbon = int(hoenn_ribbons[15], 2)
                                pokemon.winning_ribbon = int(hoenn_ribbons[16], 2)
                                pokemon.victory_ribbon = int(hoenn_ribbons[17], 2)
                                pokemon.artist_ribbon = int(hoenn_ribbons[18], 2)
                                pokemon.effort_ribbon = int(hoenn_ribbons[19], 2)
                                pokemon.battle_champion_ribbon = int(hoenn_ribbons[20], 2)
                                pokemon.regional_champion_ribbon = int(hoenn_ribbons[21], 2)
                                pokemon.national_champion_ribbon = int(hoenn_ribbons[22], 2)
                                pokemon.country_ribbon = int(hoenn_ribbons[23], 2)
                                pokemon.national_ribbon = int(hoenn_ribbons[24], 2)
                                pokemon.earth_ribbon = int(hoenn_ribbons[25], 2)
                                pokemon.world_ribbon = int(hoenn_ribbons[26], 2)
                                pokemon.obedience = int(hoenn_ribbons[31], 2)

                                flags = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x40+offset, 1, True))[2:].zfill(8)
                                pokemon.fateful_encounter = int(flags[0], 2)
                                pokemon.gender = int(flags[1], 2) | int(flags[2], 2)*2 
                                pokemon.alternate_form = int(flags[3:7], 2)

                                shiny_leaf_flag = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x41+offset, 1, True))[2:].zfill(8)
                                pokemon.shiny_leaf_1 = int(shiny_leaf_flag[0], 2)
                                pokemon.shiny_leaf_1 = int(shiny_leaf_flag[1], 2)
                                pokemon.shiny_leaf_1 = int(shiny_leaf_flag[2], 2)
                                pokemon.shiny_leaf_1 = int(shiny_leaf_flag[3], 2)
                                pokemon.shiny_crown = int(shiny_leaf_flag[4], 2)

                                if version in (9, 10):
                                    pokemon.met_location = ByteUtility.get_int(substructure_bytes_decrypted, 0x44+offset, 2, True)
                                    pokemon.egg_hatch_location = ByteUtility.get_int(substructure_bytes_decrypted, 0x6+offset, 2, True)
                                continue

                            case "C":
                                offset -= 64
                                pokemon.nickname = ByteUtility.get_encoded_string(ByteUtility.get_bytes(substructure_bytes_decrypted, offset+0x48, 0x5D-0x48), version, lang)
                                pokemon.origin_game = ByteUtility.get_int(substructure_bytes_decrypted, offset+0x5f, 1, True)
                                pokemon.sinnoh_ribbons_2 = ByteUtility.get_int(substructure_bytes_decrypted, offset+0x60, 4, True)
                                continue

                            case "D":
                                offset -= 96
                                pokemon.trainer_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(substructure_bytes_decrypted, offset+0x68, 0x77-0x68), version, lang)
                                pokemon.egg_receive_date = ByteUtility.get_bytes(substructure_bytes_decrypted, offset+0x78, 0x7A-0x78)
                                pokemon.met_date = ByteUtility.get_bytes(substructure_bytes_decrypted, offset+0x7b, 0x7d-0x7b)

                                if version == 8:
                                    pokemon.met_location = ByteUtility.get_int(substructure_bytes_decrypted, 0x80+offset, 2, True)
                                    pokemon.egg_hatch_location = ByteUtility.get_int(substructure_bytes_decrypted, 0x7e+offset, 2, True)

                                pokemon.pokerus = ByteUtility.get_int(substructure_bytes_decrypted, offset+0x82, 1, True)
                                pokemon.pokeball = ByteUtility.get_int(substructure_bytes_decrypted, offset+0x83, 1, True)

                                if version == 10:
                                    pokemon.pokeball = ByteUtility.get_int(substructure_bytes_decrypted, offset+0x86, 1, True)
                                    pokemon.walking_mood = ByteUtility.get_int(substructure_bytes_decrypted, offset+0x87, 1, True)

                                origin_flag = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x84+offset, 1, True))[2:].zfill(8)
                                pokemon.level_met = int(origin_flag[0:6], 2)
                                pokemon.trainer_gender = int(origin_flag[7], 2)
                                pokemon.encounter_type = ByteUtility.get_int(substructure_bytes_decrypted, 0x85+offset, 1, True)
                                continue

                            case _:
                                pass

                    # static encrypted bytes
                    # decryption
                    battle_stats_encrypted = ByteUtility.get_bytes(pokemon_bytes, 0x88, 0xeb-0x88)

                    prng = pokemon.personality_value
                    word_size = 2
                    battle_stats_decrypted = b''
                    for i in range(64*word_size):
                        if i % word_size == 0:
                            prng = ((0x41C64E6D * prng) + 0x6073) 
                            rand = prng >> 16
                            y = ByteUtility.get_int(battle_stats_encrypted, i, word_size, True)
                            unencrypted = (y ^ rand) & 0xffff
                            battle_stats_decrypted += unencrypted.to_bytes(word_size, 'little')    

                    offset = 0 - 0x88
                    pokemon.level = ByteUtility.get_int(battle_stats_decrypted, offset+0x8c, 1, True)
                    pokemon.seals = ByteUtility.get_int(battle_stats_decrypted, offset+0x8d, 1, True)
                    pokemon.seal_coordinates = ByteUtility.get_int(battle_stats_decrypted, offset+0xd4, 0xeb-0xd4, True)
                    pokemon.mail_id = len(ByteUtility.get_bytes(battle_stats_decrypted, offset+0x9c, 0xd3-0x9c))
                    pokemon.hp_stat = ByteUtility.get_int(battle_stats_decrypted, offset+0x90, 2, True)
                    pokemon.attack_stat = ByteUtility.get_int(battle_stats_decrypted, offset+0x92, 2, True)
                    pokemon.defense_stat = ByteUtility.get_int(battle_stats_decrypted, offset+0x94, 2, True)
                    pokemon.speed_stat = ByteUtility.get_int(battle_stats_decrypted, offset+0x96, 2, True)
                    pokemon.special_attack_stat = ByteUtility.get_int(battle_stats_decrypted, offset+0x98, 2, True)
                    pokemon.special_defense_stat = ByteUtility.get_int(battle_stats_decrypted, offset+0x9a, 2, True)
                    party.append(pokemon)
                return party

            case 7:
                print("working with DPPHGSS")
            case 7:
                print("Working with BWB2W2")
            case _:
                print("Unknown option")
