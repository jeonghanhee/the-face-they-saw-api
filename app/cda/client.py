from app.scenario import Scenario

class Client:
    id: str
    scenario: Scenario

    def __init__(self, id: str):
        self.id = id
        self.scenario = None

    def set_scenario(self, scenario: Scenario):
        self.scenario = scenario