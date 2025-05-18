from Lookup import Lookup
from Models.Enum import Gender


class Trainer:
    name: str
    gender: Gender
    public_id: int
    secret_id: int

    def __init__(self, name: str, gender: int, public_id: int, secret_id: int):
        self.name = name
        self.gender = Gender(gender)
        self.public_id = public_id
        self.secret_id = secret_id

    def __str__(self):
        return f"{self.name} ({self.gender.name}) ID:{self.public_id}_{self.secret_id}"
