import datetime
import math
import os
import random
import re
from ByteUtility import ByteUtility
from Lookup import Lookup
from Models.Enum import Gender
from Models.Trainer import Trainer

class Origin:
    fateful_encounter: bool
    egg_hatch_location: int
    egg_receive_date: int
    met_date: int
    encounter_type: int
    pokeball: int
    origin_game: int
    met_level: int
    catch_datetime: datetime.datetime
    catch_level: int
    catch_location: str
    met_location: str

    def __init__(self):
        self.fateful_encounter = False
        self.egg_hatch_location = 0
        self.egg_receive_date = 0
        self.met_date = 0
        self.encounter_type = 0
        self.pokeball = 0
        self.origin_game = 0
        self.met_level = 1
        self.catch_datetime = datetime.datetime.strptime("2000/01/01 00:00:00", "%Y/%m/%d %H:%M:%S")
        pass

    def __str__(self):
        return f"Met at Lv.{self.met_level}"
    

class Move:
    id: int
    identifer: str
    pp: int
    times_increased: int

    def __init__(self, id, pp, times_increased):
        self.id = id
        self.identifer = Lookup.moves.get(id, "")
        self.pp = pp
        self.times_increased = times_increased
        
    def __str__(self):
        if self.id == 0:
            return ""
        else:
            return f"{self.id}:{self.identifer} ({self.pp}p{self.times_increased})"
    
    def __repr__(self):
        return self.__str__()
    

class Stat:
    value: int
    ev: int
    iv: int

    def __init__(self, value, ev, iv):
        self.value = value
        self.ev = ev
        self.iv = iv

    def __str__(self):
        return f"{self.value}, Exp:{self.ev}, IV:{self.iv}"
    

class RibbonSet:
    # sinnoh set 1
    sinnoh_champ: bool
    ability: bool
    great_ability: bool
    double_ability: bool
    multi_ability: bool
    pair_ability: bool
    world_ability: bool
    alert: bool
    shock: bool
    downcast: bool
    careless: bool
    relax: bool
    snooze: bool
    smile: bool
    gorgeous: bool
    royal: bool
    gorgeous_royal: bool
    footprint: bool
    record: bool
    history: bool
    legend: bool
    red: bool
    green: bool
    blue: bool
    fesstival: bool
    carnival: bool
    classic: bool
    premier: bool

    # sinnoh set 2
    sinnoh_cool: bool
    sinnoh_cool_great: bool
    sinnoh_cool_ultra: bool
    sinnoh_cool_master: bool
    sinnoh_beauty: bool
    sinnoh_beauty_great: bool
    sinnoh_beauty_ultra: bool
    sinnoh_beauty_master: bool
    sinnoh_cute: bool
    sinnoh_cute_great: bool
    sinnoh_cute_ultra: bool
    sinnoh_cute_master: bool
    sinnoh_smart: bool
    sinnoh_smart_great: bool
    sinnoh_smart_ultra: bool
    sinnoh_smart_master: bool
    sinnoh_tough: bool
    sinnoh_tough_great: bool
    sinnoh_tough_ultra: bool
    sinnoh_tough_master: bool

    # heonn set
    heonn_cool: bool
    heonn_cool_super: bool
    heonn_cool_hyper: bool
    heonn_cool_master: bool
    heonn_beauty: bool
    heonn_beauty_super: bool
    heonn_beauty_hyper: bool
    heonn_beauty_master: bool
    heonn_cute: bool
    heonn_cute_super: bool
    heonn_cute_hyper: bool
    heonn_cute_master: bool
    heonn_smart: bool
    heonn_smart_super: bool
    heonn_smart_hyper: bool
    heonn_smart_master: bool
    heonn_tough: bool
    heonn_tough_super: bool
    heonn_tough_hyper: bool
    heonn_tough_master: bool
    champion: bool
    winning: bool
    victory: bool
    artist: bool
    effort: bool
    marine: bool
    land: bool
    sky: bool
    country: bool
    national: bool
    earth: bool
    world: bool

    def __init__(self):
        for k in self.__dict__.keys():
            self.__dict__[k] = False

    def __str__(self):
        return f""
    

class Markings:
    circle: bool
    square: bool
    trinagle: bool
    heart: bool
    star: bool
    diamond: bool

    def __init__(self, generation, byte):
        if generation == 3:
            self.circle = bool(ByteUtility.get_bit(byte,0))
            self.square = bool(ByteUtility.get_bit(byte,1))
            self.trinagle = bool(ByteUtility.get_bit(byte,2))
            self.heart = bool(ByteUtility.get_bit(byte,3))
        else:
            self.circle = bool(ByteUtility.get_bit(byte,0))
            self.trinagle = bool(ByteUtility.get_bit(byte,1))
            self.square = bool(ByteUtility.get_bit(byte,2))
            self.heart = bool(ByteUtility.get_bit(byte,3))
            self.star = bool(ByteUtility.get_bit(byte,4))
            self.diamond = bool(ByteUtility.get_bit(byte,5))

    def __str__(self):
        result = []
        if self.circle:
            result.append("CIRCLE")
        if self.square:
            result.append("SQUARE")
        if self.trinagle:
            result.append("TRIANGLE")
        if self.heart:
            result.append("HEART")
        if self.star:
            result.append("STAR")
        if self.diamond:
            result.append("DIAMOND")
        return ";".join(result)

class Pokemon:

    # game
    generation: int
    language: str

    # overview
    species_id: int
    alternate_form_id: int
    personality_value: int
    is_egg: bool
    origin: Origin
    original_trainer: Trainer

    # nickname
    has_nickname: bool
    nickname: str

    # status
    level: int
    experience_points: int
    held_item: int
    friendship: int
    walking_mood: int

    # stats
    hp: Stat
    attack: Stat
    defense: Stat
    speed: Stat
    special_attack: Stat
    special_defense: Stat
    moves: dict[int, Move]
    pokerus: bool
    pokerus_days_remaining: int
    pokerus_strain: int
    
    # other
    coolness: int
    beauty: int
    cuteness: int
    smartness: int
    toughness: int
    sheen: int
    obedience: int
    ribbons: RibbonSet
    sheen: int
    markings: Markings
    seals: int
    seal_coordinates: int
    shiny_leaf_1: bool
    shiny_leaf_2: bool
    shiny_leaf_3: bool
    shiny_leaf_4: bool
    shiny_crown: bool

    def __init__(self, generation):
        # game
        self.generation = generation
        self.language = "EN"

        # overview
        self.original_trainer = Trainer("PROF.OAK", 0, 1, 1)
        self.species_id = 0
        self.alternate_form_id = 0
        
        self.personality_value = 0
        self.is_egg = False
        self.ability = ""

        # nickname
        self.has_nickname = False
        self.nickname = ""

        # status
        self.level = 1
        self.experience_points = 0
        self.held_item = 0
        self.friendship = 0
        self.walking_mood = 0

        # stats
        self.attack = Stat(0,0,0)
        self.defense = Stat(0,0,0)
        self.speed = Stat(0,0,0)
        self.special_attack = Stat(0,0,0)
        self.special_defense = Stat(0,0,0)
        self.moves = {}
        self.pokerus = False
        self.pokerus_days_remaining = 0
        self.pokerus_strain = 0

        self.coolness = 0
        self.beauty = 0
        self.cuteness = 0
        self.smartness = 0
        self.toughness = 0
        self.sheen = 0
        self.obedience = 0
        self.ribbons = RibbonSet()
        self.sheen = 0
        self.markings = Markings(generation, b'\x00')
        self.origin = Origin()
        self.seals = b'\x00'
        self.seal_coordinates = b'\x00'
        self.shiny_leaf_1 = False
        self.shiny_leaf_2 = False
        self.shiny_leaf_3 = False
        self.shiny_leaf_4 = False
        self.shiny_crown = False


    def console_print(self):
        print(
            f"{self.species_id}: {Lookup.get_species_name(self.species_id)} Form:{self.alternate_form_id} Gen:{self.generation} Lang:{self.language}",
            f"\tHasNickname:{self.has_nickname} Nickname:[{self.nickname}]",
            f"\tOT:{self.original_trainer} Item:{Lookup.get_item_name(self.held_item)}",
            f"\tLv.{self.level} Exp:{self.experience_points} Frnd:{self.friendship} WalkMood:{self.walking_mood} Ob:{self.obedience} IsEgg:{self.is_egg}",
            f"\tPv:{self.get_personality_string()} : {self.personality_value}",
            f"\t\tGender:{self.get_gender_by_personality_value().name} Ability:{Lookup.get_ability_name(self.get_ability_from_personality_value())} Nature:{Lookup.get_nature_name(self.get_nature_from_personality_value())} Shiny:{self.get_shiny_from_personality_value()}",
            f"\tPokerus:{self.pokerus} Rem:{self.pokerus_days_remaining} Str:{self.pokerus_strain}",
            f"\tOrigin:{self.origin}",
            f"\tContest: Cool:{self.coolness} Beauty:{self.beauty} Cute:{self.cuteness} Smart:{self.smartness} Tough:{self.toughness} Sheen{self.sheen}",
            f"\tRibbons:{self.ribbons}",
            f"\tSeals: {bin(ByteUtility.get_int(self.seals, 0, len(self.seals), True))[2:].zfill(len(self.seals)*8)} Coordinates: {bin(ByteUtility.get_int(self.seal_coordinates, 0, len(self.seal_coordinates), True))[2:].zfill(len(self.seal_coordinates)*8)}",
            f"\tShinyLeafs:{self.shiny_leaf_1}:{self.shiny_leaf_2}:{self.shiny_leaf_3}:{self.shiny_leaf_4} Crown:{self.shiny_crown}",
            f"\tMarkings:{self.markings}",
            f"\tAtk:{self.attack}",
            f"\tDef:{self.defense}",
            f"\tSpe:{self.speed}",
            f"\tSpA:{self.special_attack}",
            f"\tSpD:{self.special_defense}",
            f"\tM1:{self.moves.get(0, '')}",
            f"\tM2:{self.moves.get(1, '')}",
            f"\tM3:{self.moves.get(2, '')}",
            f"\tM4:{self.moves.get(3, '')}",
        sep=os.linesep)

    # personality assignments and results
    def get_personality_value(self) -> int:
        return random.randint(0, 2**32)
    
    def get_personality_string(self):
        binary = bin(self.personality_value)[2:].zfill(32)
        return " ".join(binary[i:i+8] for i in range(0, len(binary), 8))

    def get_gender_by_personality_value(self) -> Gender:
        p_gender = self.personality_value % 256
        threshold = Lookup.get_gender_threshold(self.species_id)
        if threshold == 0:
            return Gender.MALE
        elif threshold == 254:
            return Gender.FEMALE
        elif threshold == 255:
            return Gender.GENDERLESS
        else:
            if p_gender >= threshold:
                return Gender.MALE
            else:
                return Gender.FEMALE
            
    def get_gender_by_iv(self):
        ratio = Lookup.get_gender_rate(self.species_id)
        if ratio == 1:
            return Gender.MALE
        elif ratio == 8:
            return Gender.FEMALE
        elif ratio == -1:
            return Gender.GENDERLESS
        else:
            return Gender.FEMALE if self.attack.iv <= ratio else Gender.MALE 

            
    def get_ability_from_personality_value(self) -> int:
        possible_abilities = Lookup.get_abilities(self.species_id)
        if len(possible_abilities) == 2 and possible_abilities[0] != 0:
            if possible_abilities[1] == 0:
                return possible_abilities[0]
            else:
                choice = self.personality_value % 1
                return possible_abilities[choice]
        else:
            return 0
        
    def get_nature_from_personality_value(self) -> int:
        p_nature = self.personality_value % 25
        return Lookup.get_nature_id_by_index(p_nature)
    
    def get_shiny_from_personality_value(self) -> bool:
        p1 = math.floor(self.personality_value / 65536) 
        p2 = self.personality_value % 65536
        shiny_value = self.original_trainer.public_id ^ self.original_trainer.secret_id ^ p1 ^ p2
        return shiny_value < 8
    
    def check_if_nickname(self):
        return re.sub(r"[^0-9a-zA-Z\w]+", "", self.nickname.lower().replace(" ","-")) != Lookup.get_species_name(self.species_id).lower()

    
    # Decoding
    # https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_I)
    def load_from_gen1_bytes(self, content: bytes, version: int, nickname, trainer_name):
        self.nickname = nickname
        self.original_trainer = Trainer(trainer_name, 0, ByteUtility.get_int(content, 0x0C, 2), ByteUtility.get_int(content, 0x0C, 2, True))
        self.species_id = Lookup.get_species_id_by_index(1, ByteUtility.get_int(content, 0, 1))
        self.level = ByteUtility.get_int(content, 0x21, 1)
        self.experience_points = ByteUtility.get_int(content, 0x0E, 3)
        self.has_nickname = self.check_if_nickname()
        self.personality_value = self.get_personality_value()
        self.friendship = Lookup.get_base_happiness(self.species_id)

        # get moves
        pp1 = bin(ByteUtility.get_int(content, 0x1D, 1))[2:].zfill(8)
        self.moves[0] = Move(ByteUtility.get_int(content, 0x08, 1), int(pp1[2:8], 2), int(pp1[0:2], 2))

        pp2 = bin(ByteUtility.get_int(content, 0x1E, 1))[2:].zfill(8)
        self.moves[1] = Move(ByteUtility.get_int(content, 0x09, 0x01), int(pp2[2:8], 2), int(pp2[0:2], 2))

        pp3 = bin(ByteUtility.get_int(content, 0x1F, 1))[2:].zfill(8)
        self.moves[2] = Move(ByteUtility.get_int(content, 0x0A, 0x01), int(pp3[2:8], 2), int(pp3[0:2], 2))

        pp4 = bin(ByteUtility.get_int(content, 0x20, 1))[2:].zfill(8)
        self.moves[3] = Move(ByteUtility.get_int(content, 0x0B, 0x01), int(pp4[2:8], 2), int(pp4[0:2], 2))

        # get stats
        bits = bin(ByteUtility.get_int(content, 0x1B, 2))[2:]
        iv_stats = [bits[i:i+4] for i in range(0, len(bits), 4)]

        self.hp = Stat(ByteUtility.get_int(content, 0x22, 2), ByteUtility.get_int(content, 0x11, 2), 0)
        self.attack = Stat(ByteUtility.get_int(content, 0x24, 2), ByteUtility.get_int(content, 0x13, 2), int(iv_stats[0], 2))
        self.defense = Stat(ByteUtility.get_int(content, 0x26, 2), ByteUtility.get_int(content, 0x15, 2), int(iv_stats[1], 2))
        self.speed = Stat(ByteUtility.get_int(content, 0x28, 2), ByteUtility.get_int(content, 0x17, 2), int(iv_stats[2], 2))
        self.special_attack = Stat(ByteUtility.get_int(content, 0x2A, 2), ByteUtility.get_int(content, 0x19, 2), int(iv_stats[3], 2))
        self.special_defense = Stat(ByteUtility.get_int(content, 0x2A, 2), ByteUtility.get_int(content, 0x19, 2), int(iv_stats[3], 2))        


    # https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_II)
    def load_from_gen2_bytes(self, content: bytes, version: int, nickname, trainer_name):
        self.nickname = nickname
        self.level = ByteUtility.get_int(content, 0x1F, 1)
        self.experience_points = ByteUtility.get_int(content, 0x08, 3)
        self.species_id = ByteUtility.get_int(content, 0x00, 1)
        self.has_nickname = self.check_if_nickname()
        self.personality_value = self.get_personality_value()
        self.friendship = ByteUtility.get_int(content, 0x1B, 1)
        self.held_item = Lookup.get_item_id_by_index(2, ByteUtility.get_int(content, 0x01, 1))

        # get moves
        pp1 = bin(ByteUtility.get_int(content, 0x17, 1))[2:].zfill(8)
        self.moves[0] = Move(ByteUtility.get_int(content, 0x02, 1), int(pp1[2:8], 2), int(pp1[0:2], 2))

        pp2 = bin(ByteUtility.get_int(content, 0x18, 1))[2:].zfill(8)
        self.moves[1] = Move(ByteUtility.get_int(content, 0x03, 0x01), int(pp2[2:8], 2), int(pp2[0:2], 2))

        pp3 = bin(ByteUtility.get_int(content, 0x19, 1))[2:].zfill(8)
        self.moves[2] = Move(ByteUtility.get_int(content, 0x04, 0x01), int(pp3[2:8], 2), int(pp3[0:2], 2))

        pp4 = bin(ByteUtility.get_int(content, 0x1A, 1))[2:].zfill(8)
        self.moves[3] = Move(ByteUtility.get_int(content, 0x05, 0x01), int(pp4[2:8], 2), int(pp4[0:2], 2))

        # get stats
        bits = bin(ByteUtility.get_int(content, 0x15, 2))[2:].zfill(16)
        iv_stats = [bits[i:i+4] for i in range(0, len(bits), 4)]

        self.hp = Stat(ByteUtility.get_int(content, 0x24, 2), ByteUtility.get_int(content, 0x0B, 2), 0)
        self.attack = Stat(ByteUtility.get_int(content, 0x26, 2), ByteUtility.get_int(content, 0x0D, 2), int(iv_stats[0], 2))
        self.defense = Stat(ByteUtility.get_int(content, 0x28, 2), ByteUtility.get_int(content, 0x0F, 2), int(iv_stats[1], 2))
        self.speed = Stat(ByteUtility.get_int(content, 0x2A, 2), ByteUtility.get_int(content, 0x11, 2), int(iv_stats[2], 2))
        self.special_attack = Stat(ByteUtility.get_int(content, 0x2C, 2), ByteUtility.get_int(content, 0x13, 2), int(iv_stats[3], 2))
        self.special_defense = Stat(ByteUtility.get_int(content, 0x2E, 2), ByteUtility.get_int(content, 0x15, 2), int(iv_stats[3], 2))

        # pokerus
        pokerus_data = ByteUtility.get_int(content, 0x1C, 1)
        self.pokerus_strain = (pokerus_data >> 4) != 0
        self.pokerus_days_remaining = pokerus_data % 16
        self.pokerus = self.pokerus_strain != 0

        # origin
        origin_bits = bin(ByteUtility.get_int(content, 0x1D, 2))[2:].zfill(16)
        time_of_day = int(origin_bits[0:2], 2)
        if time_of_day == 1:
            self.origin.catch_datetime.replace(hour=8)
        elif time_of_day == 2:
            self.origin.catch_datetime.replace(hour=14)
        elif time_of_day == 3:
            self.origin.catch_datetime.replace(hour=20)
        self.origin.met_level = max(int(origin_bits[2:7], 2), 2)
        self.origin.met_location = int(origin_bits[9:15], 2)
        self.original_trainer = Trainer(trainer_name, int(origin_bits[8], 2), ByteUtility.get_int(content, 0x06, 2), ByteUtility.get_int(content, 0x06, 2, True))
        if version == 4 and self.original_trainer.public_id % 1 == 1:
            self.original_trainer.gender = Gender.FEMALE
        
    def load_from_gen3_bytes(self, content: bytes, version: int, lang: str):
        self.personality_value = ByteUtility.get_int(content, 0x00, 4, True)
        self.trainer_id = ByteUtility.get_int(content, 0x04, 2, True)
        self.nickname = ByteUtility.get_encoded_string(ByteUtility.get_bytes(content, 0x08, 10), version, lang)
        self.language = ByteUtility.get_int(content, 0x12, 1, True)
        self.trainer_name = ByteUtility.get_encoded_string(ByteUtility.get_bytes(content, 0x14, 7), version, lang)
        self.markings = ByteUtility.get_int(content, 0x1b, 1, True)
        self.level = ByteUtility.get_int(content, 0x54, 1, True)
        self.mail_id = ByteUtility.get_int(content, 0x55, 1, True)
        self.hp_stat = ByteUtility.get_int(content, 0x58, 2, True)
        self.attack_stat = ByteUtility.get_int(content, 0x5a, 2, True)
        self.defense_stat = ByteUtility.get_int(content, 0x5c, 2, True)
        self.speed_stat = ByteUtility.get_int(content, 0x5e, 2, True)
        self.special_attack_stat = ByteUtility.get_int(content, 0x60, 2, True)
        self.special_defense_stat = ByteUtility.get_int(content, 0x62, 2, True)
        checksum = ByteUtility.get_int(content, 0x1c, 2, True)

        # data substructure
        print(self.nickname)
        substructure_bytes_encrypted = ByteUtility.get_bytes(content, 0x20, 48)
        order = ByteUtility.get_int(content, 0x00, 4, True) % 24
        print(order)
        
        order = {
            0: "GAEM", 1:"GAME", 2:"GEAM", 3:"GEMA",
            4: "GMAE", 5:"GMEA", 6:"AGEM", 7:"AGME",
            8: "AEGM", 9:"AEMG",10:"AMGE",11:"AMEG",
            12:"AGAM",13:"EGMA",14:"EAGM",15:"EAMG",
            16:"EMGA",17:"EMAG",18:"MGAE",19:"MGEA",
            20:"MAGE",21:"MAEG",22:"MEGA",23:"MEAG"
        }

        order_string = order[order]
        print(f"Order:{order}:{order_string}")
        decryption_key = bytes(a ^ b for a, b in zip(ByteUtility.get_bytes(content, 0x04, 4), ByteUtility.get_bytes(content, 0x00, 4)))
        print(f"Decryption:{ByteUtility.get_int(decryption_key, 0,4)}")
        substructure_bytes_decrypted = b''
        for i in range(48):
            if i % 4 == 0:
                y = ByteUtility.get_bytes(substructure_bytes_encrypted, 0x1*i, 4)
                unencrypted = bytes(a ^ b for a, b in zip(y, decryption_key))
                substructure_bytes_decrypted += unencrypted
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
                    self.species_id = Lookup.pokemon_gen3_index.get(ByteUtility.get_int(substructure_bytes_decrypted, 0x0+offset, 2, True),0)
                    self.held_item = ByteUtility.get_int(substructure_bytes_decrypted, 0x2+offset, 2, True)
                    self.experience_points = ByteUtility.get_int(substructure_bytes_decrypted, 0x4+offset, 4, True)
                    self.friendship = ByteUtility.get_int(substructure_bytes_decrypted, 0x9+offset, 1, True)

                    pp_bonuses = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x08+offset, 1, True))[2:].zfill(8)
                    self.move1_pp_times = int(pp_bonuses[0:2], 2)
                    self.move2_pp_times = int(pp_bonuses[2:4], 2)
                    self.move3_pp_times = int(pp_bonuses[4:6], 2)
                    self.move4_pp_times = int(pp_bonuses[6:8], 2)
                    continue

                case "A":
                    self.move1 = ByteUtility.get_int(substructure_bytes_decrypted, 0x0+offset, 2, True)
                    self.move2 = ByteUtility.get_int(substructure_bytes_decrypted, 0x2+offset, 2, True)
                    self.move3 = ByteUtility.get_int(substructure_bytes_decrypted, 0x4+offset, 2, True)
                    self.move4 = ByteUtility.get_int(substructure_bytes_decrypted, 0x6+offset, 2, True)
                    self.move1_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x8+offset, 1, True)
                    self.move2_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0x9+offset, 1, True)
                    self.move3_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0xA+offset, 1, True)
                    self.move4_pp = ByteUtility.get_int(substructure_bytes_decrypted, 0xB+offset, 1, True)
                    continue

                case "E":
                    self.hp_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x0+offset, 1, True)
                    self.attack_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x1+offset, 1, True)
                    self.defense_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x2+offset, 1, True)
                    self.speed_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x3+offset, 1, True)
                    self.special_attack_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x4+offset, 1, True)
                    self.special_defense_stat_experience = ByteUtility.get_int(substructure_bytes_decrypted, 0x5+offset, 1, True)
                    self.coolness = ByteUtility.get_int(substructure_bytes_decrypted, 0x6+offset, 1, True)
                    self.beauty = ByteUtility.get_int(substructure_bytes_decrypted, 0x7+offset, 1, True)
                    self.cuteness = ByteUtility.get_int(substructure_bytes_decrypted, 0x8+offset, 1, True)
                    self.smartness = ByteUtility.get_int(substructure_bytes_decrypted, 0x9+offset, 1, True)
                    self.toughness = ByteUtility.get_int(substructure_bytes_decrypted, 0xA+offset, 1, True)
                    self.sheen = ByteUtility.get_int(substructure_bytes_decrypted, 0xB+offset, 1, True)
                    continue

                case "M":
                    pokerus = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x0+offset, 1, True))[2:].zfill(8)
                    self.pokerus = int(pokerus[4:8], 2)
                    self.pokerus_days_remaining = int(pokerus[0:4], 2)
                    self.met_location = ByteUtility.get_int(substructure_bytes_decrypted, 0x1+offset, 1, True)

                    origins = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x2+offset, 2, True))[2:].zfill(16)
                    self.trainer_gender = int(origins[15], 2)
                    self.pokeball = int(origins[11:14], 2)
                    self.origin_game = int(origins[7:10], 2)
                    self.level_met = int(origins[0:6], 2)

                    iv_egg_ability = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x4+offset, 4, True))[2:].zfill(32)
                    self.hp_iv = int(iv_egg_ability[0:4], 2)
                    self.attack_iv = int(iv_egg_ability[5:9], 2)
                    self.defense_iv = int(iv_egg_ability[10:14], 2)
                    self.speed_iv = int(iv_egg_ability[15:19], 2)
                    self.special_attack_iv = int(iv_egg_ability[20:24], 2)
                    self.special_defense_iv = int(iv_egg_ability[25:29], 2)
                    self.is_egg = int(iv_egg_ability[30], 2)
                    self.ability = int(iv_egg_ability[31], 2)

                    ribbons_obedience = bin(ByteUtility.get_int(substructure_bytes_decrypted, 0x8+offset, 4, True))[2:].zfill(32)
                    self.cool_ribbon = int(ribbons_obedience[0:2], 2)
                    self.beauty_ribbon = int(ribbons_obedience[3:5], 2)
                    self.cute_ribbon = int(ribbons_obedience[6:8], 2)
                    self.smart_ribbon = int(ribbons_obedience[9:11], 2)
                    self.tough_ribbon = int(ribbons_obedience[12:14], 2)
                    self.champion_ribbon = int(ribbons_obedience[15], 2)
                    self.winning_ribbon = int(ribbons_obedience[16], 2)
                    self.victory_ribbon = int(ribbons_obedience[17], 2)
                    self.artist_ribbon = int(ribbons_obedience[18], 2)
                    self.effort_ribbon = int(ribbons_obedience[19], 2)
                    self.battle_champion_ribbon = int(ribbons_obedience[20], 2)
                    self.regional_champion_ribbon = int(ribbons_obedience[21], 2)
                    self.national_champion_ribbon = int(ribbons_obedience[22], 2)
                    self.country_ribbon = int(ribbons_obedience[23], 2)
                    self.national_ribbon = int(ribbons_obedience[24], 2)
                    self.earth_ribbon = int(ribbons_obedience[25], 2)
                    self.world_ribbon = int(ribbons_obedience[26], 2)
                    self.obedience = int(ribbons_obedience[31], 2)
                    continue