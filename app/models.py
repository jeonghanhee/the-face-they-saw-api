from dataclasses import dataclass
from korean_name_generator import namer
import random

from app.enums import SKETCH_LEVEL_ATTRS, Personality, random_enum

@dataclass
class Witness:
    name: str
    gender: str
    personality: str

@dataclass
class CompositeSketch:
    face_shape: str = ""
    eyes_of: str = ""
    nose_and_mouth: str = ""
    style: str = ""
    singularity: str = ""

    @property
    def cumulative_description(self) -> str:
        fields = [self.face_shape, self.eyes_of, self.nose_and_mouth, self.style, self.singularity]
        return "\n".join([f"- {f}" for f in fields if f])

@dataclass
class Scenario:
    witness: Witness
    composite_sketch: CompositeSketch
    crime_type: str
    place: str
    timezone: str
    statement: str

def build_witness() -> Witness:
    is_female = random.choice([True, False])
    return Witness(
        name=namer.generate(not is_female),
        gender="여성" if is_female else "남성",
        personality=random_enum(Personality),
    )


def build_composite_sketch(level: int) -> CompositeSketch:
    sketch = CompositeSketch()
    for attr, pool in SKETCH_LEVEL_ATTRS[:level]:
        setattr(sketch, attr, random.choice(pool))
    return sketch