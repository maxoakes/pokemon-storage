from ByteUtility import ByteUtility
from Models.Enum import Gender
from Models.Game import Game
from Models.Pokemon import Pokemon
from Models.Trainer import Trainer


class GameState:
    target_box: int
    target_slot: int
    content: bytes
    game: Game
    lang: str
    trainer: Trainer
    party: dict[int, Pokemon]
    box_lists: dict[int, dict[int, Pokemon]]

    def __init__(self, content: bytes, game: Game, lang: str):
        self.content = content
        self.game = game
        self.lang = lang
        self.party = []
        self.box_lists = {}

        version = game.version_id
        match version:
            # Generation 1, big-endian
            case 1 | 2:
                player_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(content, 0x2598, 11), version, lang)
                self.trainer = Trainer(player_name, 0, ByteUtility.get_int(content, 0x2605, 2), 0)

                party_bytes = ByteUtility.get_bytes(content, 0x2F2C, 0x194)
                self.party = GameState.get_gen1_pokemon_from_storage(party_bytes, version, lang, 0x8, 0x2C, 0x110, 0x152)

                box_size = 0x462
                box_locations = {
                    1: 0x4000,
                    2: 0x4462,
                    3: 0x48C4,
                    4: 0x4D26,
                    5: 0x5188,
                    6: 0x55EA,
                    7: 0x6000,
                    8: 0x6462,
                    9: 0x68C4,
                    10: 0x6D26,
                    11: 0x7188,
                    12: 0x75EA
                }

                for (box_id, box_offset) in box_locations.items():
                    box_bytes = ByteUtility.get_bytes(content, box_offset, box_size)
                    self.box_lists[box_id] = GameState.get_gen1_pokemon_from_storage(box_bytes, version, lang, 0x16, 0x21, 0x2AA, 0x386)

            # Generation 2, big-endian
            case 3 | 4:
                player_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(content, 0x200B, 11), version, lang)
                self.trainer = Trainer(player_name, 0, ByteUtility.get_int(content, 0x2009, 2), 0)
                if version == 4 and self.trainer.public_id % 1 == 1:
                    self.trainer.gender = Gender.FEMALE

                party_bytes = []
                if version == 3:
                    party_bytes = ByteUtility.get_bytes(content, 0x288A, 428)
                else:
                    party_bytes = ByteUtility.get_bytes(content, 0x2865, 428)

                self.party = GameState.get_gen2_pokemon_from_storage(party_bytes, version, lang, 6, 48)

                box_size = 1102
                box_locations = {
                    1: 0x4000,
                    2: 0x4450,
                    3: 0x48A0,
                    4: 0x4CF0,
                    5: 0x5140,
                    6: 0x5590,
                    7: 0x59E0,
                    8: 0x6000,
                    9: 0x6450,
                    10: 0x68A0,
                    11: 0x6CF0,
                    12: 0x7140,
                    13: 0x7590,
                    14: 0x79E0
                }

                for (box_id, box_offset) in box_locations.items():
                    box_bytes = ByteUtility.get_bytes(content, box_offset, box_size)
                    self.box_lists[box_id] = GameState.get_gen2_pokemon_from_storage(box_bytes, version, lang, 20, 32)

            case 5 | 6 | 7:
                pass
            case 8 | 9 | 10:
                pass
            case _:
                return
            

    def get_gen1_pokemon_from_storage(content: bytes, version: int, lang: str, pokemon_offset: int, pokemon_size: int, trainer_name_offset: int, nicknames_offset: int) -> dict[int, Pokemon]:
        box: dict[int, Pokemon] = {}
        box_count = ByteUtility.get_int(content, 0x00, 1)
        for i in range(box_count):
            nickname_bytes = ByteUtility.get_bytes(content, nicknames_offset+(0xB*i), 0xB)
            nickname = ByteUtility.get_encoded_string(nickname_bytes, version, lang)

            ot_name_bytes = ByteUtility.get_bytes(content, trainer_name_offset+(0xB*i), 0xB)
            ot_name = ByteUtility.get_encoded_string(ot_name_bytes, version, lang)

            pokemon_bytes = ByteUtility.get_bytes(content, pokemon_offset+(pokemon_size*i), 0x21)
            pokemon = Pokemon(1)
            pokemon.load_from_gen1_bytes(pokemon_bytes, version, nickname, ot_name)
            box[i] = pokemon

        return box
    
    
    def get_gen2_pokemon_from_storage(content: bytes, version: int, lang: str, capacity: int, pokemon_size: int):
        box: dict[int, Pokemon] = {}
        count = ByteUtility.get_int(content, 0x00, 1)
        pokemon_offset = 2+capacity
        ot_name_offset = pokemon_offset+(pokemon_size*capacity)
        nickname_offset = ot_name_offset+(capacity*11)

        for i in range(count):
            ot_name_bytes = ByteUtility.get_bytes(content, ot_name_offset+(i*11), 11)
            ot_name = ByteUtility.get_encoded_string(ot_name_bytes, version, lang)

            nickname_bytes = ByteUtility.get_bytes(content, nickname_offset+(i*11), 11)
            nickname = ByteUtility.get_encoded_string(nickname_bytes, version, lang)

            pokemon_bytes = ByteUtility.get_bytes(content, pokemon_offset+(i*pokemon_size), 32)
            pokemon = Pokemon(2)
            pokemon.load_from_gen2_bytes(pokemon_bytes, version, nickname, ot_name)
            box[i] = pokemon

        return box