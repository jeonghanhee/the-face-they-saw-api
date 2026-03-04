from dataclasses import dataclass

class CompositeSketch:
    face_shape: str # 얼굴형
    eyes_of: str # 눈과 눈매
    nose_and_mouth: str # 코와 입
    style: str # 머리와 얼굴 주변 요소
    singularity: str # 식별 가능한 특이점 (악세서리)

    def __init__(self):
        self.face_shape = ""
        self.eyes_of = ""
        self.nose_and_mouth = ""
        self.style = ""
        self.singularity = ""

    def set_face_shape(self, face_shape: str):
        self.face_shape = face_shape

    def set_eyes_of(self, eyes_of: str):
        self.eyes_of = eyes_of

    def set_nose_and_mouth(self, nose_and_mouth: str):
        self.nose_and_mouth = nose_and_mouth

    def set_style(self, style: str):
        self.style = style

    def set_singularity(self, singularity: str):
        self.singularity = singularity

    @property
    def cumulative_description(self):
        description = ""
        description += f"- {self.face_shape}\n" if self.face_shape else ""
        description += f"- {self.eyes_of}\n" if self.eyes_of else ""
        description += f"- {self.nose_and_mouth}\n" if self.nose_and_mouth else ""
        description += f"- {self.style}\n" if self.style else ""
        description += f"- {self.singularity}" if self.singularity else ""
        return description
