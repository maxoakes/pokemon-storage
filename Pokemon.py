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
        self.generation = 0
        self.species_id = 0
        self.level = 0
        self.held_item = 0
        self.move1 = 0
        self.move2 = 0
        self.move3 = 0
        self.move4 = 0
        self.trainer_id = 0
        self.trainer_name = ""
        self.experience_points = 0
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
        self.move1_pp = 0
        self.move2_pp = 0
        self.move3_pp = 0
        self.move4_pp = 0 

    def console_print(self):
        print(
            f"{self.species_id}: {Lookup.pokemon.get(self.species_id, '???')} AKA:[{self.nickname}]",
            f"\tLv.{self.level} Exp:{self.experience_points}",
            f"\tOT:{self.trainer_name}/{self.trainer_id}",
            f"\tAtk:{self.attack_stat}({self.attack_stat_experience}) IV:{self.attack_iv}",
            f"\tDef:{self.defense_stat}({self.defense_stat_experience}) IV:{self.defense_iv}",
            f"\tSpA:{self.special_attack_stat}({self.special_attack_stat_experience}) IV:{self.special_attack_iv}",
            f"\tSpD:{self.special_defense_stat}({self.special_defense_stat_experience}) IV:{self.special_defense_iv}",
            f"\tSpe:{self.speed_stat}({self.speed_stat_experience}) IV:{self.speed_iv}",
            f"\tM1:{self.move1}:{Lookup.moves.get(self.move1, '???')} ({Pokemon.parse_move_byte(self.move1_pp)[0]})",
            f"\tM2:{self.move2}:{Lookup.moves.get(self.move2, '???')} ({Pokemon.parse_move_byte(self.move2_pp)[0]})",
            f"\tM3:{self.move3}:{Lookup.moves.get(self.move3, '???')} ({Pokemon.parse_move_byte(self.move3_pp)[0]})",
            f"\tM4:{self.move4}:{Lookup.moves.get(self.move4, '???')} ({Pokemon.parse_move_byte(self.move4_pp)[0]})",
        sep=os.linesep)

    def parse_move_byte(byte: str):
        bits = bin(int.from_bytes(byte))[2:]
        bits = str.zfill(bits, 8)
        return (int(bits[2:8], 2), int(bits[0:2], 2))

    def __str__(self):
        return f"{self.species_id}: Lv.{self.level}; {self.hp_stat}/{self.attack_stat}/{self.defense_stat}/{self.special_attack_stat}/{self.special_defense_stat}/{self.speed_stat}"