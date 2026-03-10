from dataclasses import dataclass

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