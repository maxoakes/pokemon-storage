class Item:
    id: int
    name: str
    id_mapping: dict[int, int] # generation, game_index

    def __init__(self, id, identifer):
        self.id = id
        self.name = identifer
        self.id_mapping = {}