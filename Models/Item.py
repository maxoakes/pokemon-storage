class Item:
    id: int
    identifier: str
    id_mapping: dict[int, int] # generation, game_index

    def __init__(self, id, identifer):
        self.id = id
        self.identifier = identifer
        self.id_mapping = {}