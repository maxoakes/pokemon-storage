class Game:
    generation_id: int
    version_id: int
    game_id: int
    game_name: int
    id_mapping: dict[int, int]

    def __init__(self, game_id, game_name, version_id, generation_id):
        self.game_id = game_id
        self.game_name = game_name
        self.version_id = version_id
        self.generation_id = generation_id
        self.id_mapping = {}

    def __str__(self):
        return f"{self.game_name} (Generation {self.generation_id})"