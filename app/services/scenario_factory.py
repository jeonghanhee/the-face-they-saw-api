import random
from app.scenario.witness import Witness
from app.scenario.composite_sketch import CompositeSketch
from app.scenario.prompt import create_ssp, create_sup
from app.scenario import Scenario
from app.llm.gemini_client import generate_content
from app.util.name_generator import get_rand_name

# People
GENDERS = ["남성", "여성"]
PLACES = ["골목길", "폐가", "폐교", "주택", "아파트"]
TIMEZONES = ["아침", "오후", "저녁", "새벽"]

# Witness
PERSONALITIES = ["겁이 많고 소심하다", "조심스럽다", "용감하다", "자신감이 있다"]

# Composite Sketch
FACE_SHAPES = []
EYES_OFS = []
NOSE_AND_MOUTHS = []
STYLES = []
SINGULARITIES = []

MAX_LEVEL = 5
INDICDENT_TYPES = ["살인", "성폭력", "강도", "폭행", "상해"]

async def create_scenario(level: int) -> Scenario:
    if level <= 0 or level > MAX_LEVEL:
        raise TypeError("Levels must be from 1 to 5.")
    
    # 사건 정보 생성
    i_type = random.choice(INDICDENT_TYPES)
    i_place = random.choice(PLACES)
    i_timezone = random.choice(TIMEZONES)

    # 증인 생성
    witness_name = get_rand_name()
    witness_gender = random.choice(GENDERS)
    witness_personality = random.choice(PERSONALITIES)
    witness = Witness(witness_name, witness_gender, witness_personality)

    # 몽타주 생성
    composite_sketch = CompositeSketch()
    if level == 1:
        composite_sketch.set_face_shape(random.choice(FACE_SHAPES) if FACE_SHAPES else "")
    if level == 2:
        composite_sketch.eyes_of(random.choice(EYES_OFS) if EYES_OFS else "")
    if level == 3:
        composite_sketch.set_nose_and_mouth(random.choice(NOSE_AND_MOUTHS) if NOSE_AND_MOUTHS else "")
    if level == 4:
        composite_sketch.set_style(random.choice(STYLES) if STYLES else "")
    if level == 5:
        composite_sketch.set_singularity(random.choice(SINGULARITIES) if SINGULARITIES else "")

    # 시스템 프롬프트 생성
    ssp = create_ssp(
        name=witness.name,
        gender=witness.gender,
        place=i_place,
        timezone=i_timezone,
        per=witness.personality,
        cd=composite_sketch.cumulative_description
    )
    # 유저 프롬프트 생성
    scp = create_sup(name=witness.name)

    # 진술 생성
    statement = await generate_content(scp, ssp)
    if not statement:
        raise TypeError("statement is empty.")
    
    # 최종 시나리오 생성
    scenario = Scenario(
        witness=witness, 
        composite_sketch=composite_sketch,
        indicdent=i_type, 
        place=i_place, 
        timezone=i_timezone, 
        statement=statement
    )

    return scenario