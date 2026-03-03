from app.scenario import Scenario

class Client:
    id: str
    scenario: Scenario

    def __init__(self, id: str):
        self.id = id
        self.scenario = None