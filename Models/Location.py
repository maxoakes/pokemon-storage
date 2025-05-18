class Location:
    id: int
    name: str
    generation_indicies: dict[int, int]

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.generation_indicies = {}

    def __str__(self):
        return self.name
