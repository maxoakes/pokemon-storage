import os
import sys
from dotenv import load_dotenv
from Database import Database
from Extractor import Extractor
from Lookup import Lookup
from Models.GameState import GameState
from Models.Pokemon import Pokemon
from Models.Trainer import Trainer

def main():

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

    # get generation and language from command line
    lang = "en"
    mode = "export"
    game_id = 0
    # python3 main.py en read 2
    
    if len(sys.argv) > 1:
        try:
            lang = sys.argv[1]
        except:
            pass
    if len(sys.argv) > 2:
        try:
            mode = sys.argv[2]
        except:
            pass
    else:
        print("Select mode:",
              "\texport = Extract a pokemon from the party or a box",
              "\timport = Add a pokemon to a party or box",
        sep=os.linesep)
        mode = input("Selection: ")

    game = None
    original_trainer = Trainer("OAK", 0, 1, 0)
    if len(sys.argv) > 3:
        try:
            game_id = int(sys.argv[3])
            game = Lookup.games.get(game_id)
        except:
            pass

    if (game_id <= 0):
        print("Select game ID:")
        for (key, game) in Lookup.games.items():
            print(f"\t{key} = {game.game_name}")
        try:
            game_id = int(input("Game ID: "))
            game = Lookup.games.get(game_id)
        except:
            print("ERROR: Invalid selection")
            return

    filepath = None
    if len(sys.argv) > 4:
        try:
            filepath = sys.argv[4]
        except:
            pass

    if filepath == None:
        filepath = input(f"Filepath to {game}: ")

    content = None
    with open(filepath, 'rb') as f:
        content = f.read()

    print(f"Reading {game} for version {game.version_id} in '{lang}' with length {len(content)}...")
    game_state = GameState(content, game, lang)

    print("Party:")
    for (i, p) in game_state.party.items():
        print(f"  Slot {i+1}: {p.get_one_liner_description()}")
    for (b_id, box) in game_state.box_lists.items():
        print(f"Box {b_id}")
        for (i, p) in box.items():
            print(f"  Slot {i+1}: {p.get_one_liner_description()}")


if __name__ == "__main__":
    main()

