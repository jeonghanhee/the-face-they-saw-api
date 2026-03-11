from enum import Enum
import random

class CrimeType(str, Enum):
    MURDER = "살인"
    SEXUAL = "성폭력"
    ROBBERY = "강도"
    ASSAULT = "폭행"
    INJURY = "상해"

class Place(str, Enum):
    ALLEY = "골목길"
    RUINS = "폐가"
    SCHOOL = "폐교"
    HOUSE = "주택"
    APARTMENT = "아파트"

class TimeZone(str, Enum):
    MORNING = "아침"
    AFTERNOON = "오후"
    EVENING = "저녁"
    DAWN = "새벽"

class Personality(str, Enum):
    TIMID = "겁이 많고 소심하다"
    CAUTIOUS = "조심스럽다"
    BRAVE = "용감하다"
    CONFIDENT = "자신감이 있다"

SKETCH_LEVEL_ATTRS: list[tuple[str, list[str]]] = [
    ("face_shape", ["둥근형", "달걀형", "각진형", "광대 있는 편", "좁고 긴 형"]),
    ("eyes_of", ["무쌍 눈매", "다크서클", "안경 쓴 눈", "처진 눈꼬리", "날카로운 눈"]),
    ("nose_and_mouth", ["무표정한 입", "오똑한 코", "둥근 코", "얇은 입술", "도톰한 입술"]),
    ("style", ["덥수룩한 머리", "포니테일", "정갈한 가르마", "비니", "모자", "마스크 착용"]),
    ("singularity", ["눈가 흉터", "입가 점", "뿔테 안경", "무선 이어폰", "피어싱"]),
]
MAX_LEVEL = len(SKETCH_LEVEL_ATTRS)

def random_enum(enum_cls: type[Enum]) -> str:
    return random.choice(list(enum_cls)).value