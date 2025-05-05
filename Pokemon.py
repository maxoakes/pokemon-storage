import os
from Lookup import Lookup

class Pokemon:
    generation: int
    species_id: int
    level: int
    held_item: int
    move1: int
    move2: int
    move3: int
    move4: int
    nickname: str
    trainer_id: int
    trainer_name: str
    experience_points: int
    hp_stat_experience: int
    hp_stat: int
    hp_iv: int
    attack_stat: int
    attack_stat_experience: int
    attack_iv: int
    defense_stat: int
    defense_stat_experience: int
    defense_iv: int
    special_attack_stat: int
    special_attack_stat_experience: int
    special_attack_iv: int
    special_defense_stat: int
    special_defense_stat_experience: int
    special_defense_iv: int
    speed_stat: int
    speed_stat_experience: int
    speed_iv: int
    move1_pp: str
    move2_pp: str
    move3_pp: str
    move4_pp: str 

    def __init__(self, generation):
        self.generation = generation
        self.language = 0
        self.generation = 0
        self.markings = 0
        self.mail_id = 0
        self.is_egg = 0
        self.species_id = 0
        self.level = 0
        self.held_item = 0
        self.personality_value = 0
        self.ability = 0
        self.move1 = 0
        self.move2 = 0
        self.move3 = 0
        self.move4 = 0
        self.trainer_id = 0
        self.trainer_name = ""
        self.trainer_gender = 0
        self.pokeball = 0
        self.origin_game = 0
        self.level_met = 0
        self.experience_points = 0
        self.friendship = 0
        self.pokerus = 0
        self.met_location = 0
        self.pokerus_days_remaining = 0
        self.catch_time = 0
        self.catch_date = 0
        self.catch_level = 0
        self.catch_location = 0
        self.hp_stat_experience = 0
        self.hp_stat = 0
        self.hp_iv = 0
        self.attack_stat = 0
        self.attack_stat_experience = 0
        self.attack_iv = 0
        self.defense_stat = 0
        self.defense_stat_experience = 0
        self.defense_iv = 0
        self.special_attack_stat = 0
        self.special_attack_stat_experience = 0
        self.special_attack_iv = 0
        self.special_defense_stat = 0
        self.special_defense_stat_experience = 0
        self.special_defense_iv = 0
        self.speed_stat = 0
        self.speed_stat_experience = 0
        self.speed_iv = 0
        self.coolness = 0
        self.beauty = 0
        self.cuteness = 0
        self.smartness = 0
        self.toughness = 0
        self.feel = 0
        self.move1_pp = 0
        self.move2_pp = 0
        self.move3_pp = 0
        self.move4_pp = 0
        self.move1_pp_times = 0
        self.move2_pp_times = 0
        self.move3_pp_times = 0
        self.move4_pp_times = 0
        self.cool_ribbon = 0
        self.beauty_ribbon = 0
        self.cute_ribbon = 0
        self.smart_ribbon = 0
        self.tough_ribbon = 0
        self.champion_ribbon = 0
        self.winning_ribbon = 0
        self.victory_ribbon = 0
        self.artist_ribbon = 0
        self.effort_ribbon = 0
        self.battle_champion_ribbon = 0
        self.regional_champion_ribbon = 0
        self.national_champion_ribbon = 0
        self.country_ribbon = 0
        self.national_ribbon = 0
        self.earth_ribbon = 0
        self.world_ribbon = 0
        self.obedience = 0


    def console_print(self):
        print(
            f"{self.species_id}: {Lookup.pokemon.get(self.species_id, '???')} AKA:[{self.nickname}]",
            f"\tLv.{self.level} Exp:{self.experience_points}",
            f"\tOT:{self.trainer_name}/{self.trainer_id}",
            f"\tItem:{self.held_item}",
            f"\tAtk:{self.attack_stat}({self.attack_stat_experience}) IV:{self.attack_iv}",
            f"\tDef:{self.defense_stat}({self.defense_stat_experience}) IV:{self.defense_iv}",
            f"\tSpA:{self.special_attack_stat}({self.special_attack_stat_experience}) IV:{self.special_attack_iv}",
            f"\tSpD:{self.special_defense_stat}({self.special_defense_stat_experience}) IV:{self.special_defense_iv}",
            f"\tSpe:{self.speed_stat}({self.speed_stat_experience}) IV:{self.speed_iv}",
            f"\tM1:{self.move1}:{Lookup.moves.get(self.move1, '???')} ({self.move1_pp}|{self.move1_pp_times})",
            f"\tM2:{self.move2}:{Lookup.moves.get(self.move2, '???')} ({self.move2_pp}|{self.move2_pp_times})",
            f"\tM3:{self.move3}:{Lookup.moves.get(self.move3, '???')} ({self.move3_pp}|{self.move3_pp_times})",
            f"\tM4:{self.move4}:{Lookup.moves.get(self.move4, '???')} ({self.move4_pp}|{self.move4_pp_times})",
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
        return f"{self.species_id}: Lv.{self.level}; {self.hp_stat}/{self.attack_stat}/{self.defense_stat}/{self.special_attack_stat}/{self.special_defense_stat}/{self.speed_stat}"