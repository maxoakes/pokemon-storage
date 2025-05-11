import os
from ByteUtility import ByteUtility
from Lookup import Lookup
from Models.Trainer import Trainer

class Origin:
    fateful_encounter: bool
    egg_hatch_location: int
    egg_receive_date: int
    met_date: int
    encounter_type: int
    pokeball: int
    origin_game: int
    level_met: int
    catch_time: int
    catch_date: int
    catch_level: int
    catch_location: str
    met_location: str

    def __init__(self):
        pass

    def __str__(self):
        return f""
    

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
    species: str
    alternate_form_id: int
    gender: str
    personality_value: int
    is_egg: bool
    ability: str
    origin: Origin
    original_trainer: Trainer

    # nickname
    has_nickname: int
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
        self.language = ""

        # overview
        self.original_trainer = None
        self.species_id = 0
        self.species = ""
        self.alternate_form_id = 0
        
        self.gender = ""
        self.personality_value = 0
        self.is_egg = False
        self.ability = ""

        # nickname
        self.has_nickname = False
        self.nickname = ""

        # status
        self.level = 1
        self.experience_points = 0
        self.held_item = ""
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
        self.seals = b'\x00'
        self.seal_coordinates = b'\x00'
        self.shiny_leaf_1 = False
        self.shiny_leaf_2 = False
        self.shiny_leaf_3 = False
        self.shiny_leaf_4 = False
        self.shiny_crown = False


    def console_print(self):
        print(
            f"{self.species_id}: {self.species} Form:{self.alternate_form_id} Gender:{self.gender} HasNickname:{self.has_nickname} Nickname:[{self.nickname}]",
            f"\tGen:{self.generation} Lang:{Lookup.language.get(self.language, 'Unset')}",
            f"\tLv.{self.level} Exp:{self.experience_points} Frnd:{self.friendship} WalkMood:{self.walking_mood} Ob:{self.obedience} Pv:{self.personality_value} IsEgg:{self.is_egg}",
            f"\tOT:{self.original_trainer}",
            f"\tItem:{self.held_item} Ability:{self.ability}",
            f"\tPokerus:{self.pokerus} Rem:{self.pokerus_days_remaining} Str:{self.pokerus_strain}",
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

    def parse_move_byte(byte: str):
        print(type(byte))
        if type(byte) is int:
            return byte
        else:
            bits = bin(int.from_bytes(byte))[2:]
            bits = str.zfill(bits, 8)
            return (int(bits[2:8], 2), int(bits[0:2], 2))

    def __str__(self):
        return f"{self.species}: Lv.{self.level}"
    
    # Decoding
    # https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_I)
    def load_from_gen1_bytes(self, content: bytes, version: int, nickname, trainer_name):
        self.nickname = nickname
        self.trainer_name = trainer_name
        self.trainer_id = ByteUtility.get_int(content, 0x0C, 2)
        self.species_id = Lookup.pokemon_gen1_index.get(ByteUtility.get_int(content, 0, 1), 0)
        self.species = Lookup.pokemon.get(self.species_id, "???")
        self.level = ByteUtility.get_int(content, 0x21, 1)
        self.experience_points = ByteUtility.get_int(content, 0x0E, 3)

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
