import os
import sys
from dotenv import load_dotenv
from Database import Database
from Extractor import Extractor
from Lookup import Lookup
from Pokemon import Pokemon

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
    mode = "read"
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
              "\tread = Extract party from save file",
              "\ttrade = Mimic trader with game emulator",
        sep=os.linesep)
        mode = input("Selection: ")

    game = None
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

    if (mode == "trade" and game_id < 5):
        print("ERROR: Cannot trade with GB/GBC games")
        return
    
    if (mode == "read"):
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

        print(f"Reading {game} for version {game.version_id} in '{lang}' with length {len(content)}")
        party: list[Pokemon] = Extractor.get_party_from_bytes(game, lang, content)

        for p in party:
            p.console_print()

    if (mode == "trade"):
        print(f"Not implemented to trade with {Lookup.games.get(game_id)}")
        return


if __name__ == "__main__":
    main()

