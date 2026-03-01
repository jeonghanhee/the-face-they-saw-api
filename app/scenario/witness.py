from dataclasses import dataclass

@dataclass
class Witness:
    name: str
    gender: str
    personality: str

    def __init__(self, name: str, gender: str, personality: str):
        self.name = name
        self.gender = gender
        self.personality = personality