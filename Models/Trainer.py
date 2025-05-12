from Lookup import Lookup


class Trainer:
    name: str
    gender: int
    public_id: int
    secret_id: int

    def __init__(self, name: str, gender: int, public_id: int, secret_id: int):
        self.name = name
        self.gender = gender
        self.public_id = public_id
        self.secret_id = secret_id

    def __str__(self):
        return f"{self.name} ({Lookup.gender.get(self.gender)}) ID:{self.public_id}_{self.secret_id}"
