from dataclasses import dataclass
from typing import List
from app.scenario.witness import Witness
from app.scenario.composite_sketch import CompositeSketch

@dataclass
class Scenario:
    witness: Witness
    composite_sketch: CompositeSketch
    indicdent: str
    place: str
    timezone: str
    statement: List[str]

    def __init__(self, witness: Witness, composite_sketch: CompositeSketch, indicdent: str, place: str, timezone: str, statement: List[str]):
        self.witness = witness
        self.composite_sketch = composite_sketch
        self.indicdent = indicdent
        self.place = place
        self.timezone = timezone
        self.statement = statement