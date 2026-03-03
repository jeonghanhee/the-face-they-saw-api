import random
from app.scenario.witness import Witness
from app.scenario.composite_sketch import CompositeSketch
from app.scenario.prompt import create_statement_system_prompt, create_statement_user_prompt
from app.scenario import Scenario
from app.llm.gemini_client import generate_content
from korean_name_generator import namer

# 장소
PLACES = ["골목길", "폐가", "폐교", "주택", "아파트"]
# 시간대
TIMEZONES = ["아침", "오후", "저녁", "새벽"]

# 성격
PERSONALITIES = ["겁이 많고 소심하다", "조심스럽다", "용감하다", "자신감이 있다"]

# 얼굴형
FACE_SHAPES = ["둥근형", "달걀형", "각진형", "광대 있는 편", "좁고 긴 형"]
# 눈매
EYES_OFS = ["무쌍 눈매", "다크서클", "안경 쓴 눈", "처진 눈꼬리", "날카로운 눈"]
# 코와 입 주변의 특징
NOSE_AND_MOUTHS = ["무표정한 입", "오똑한 코", "둥근 코", "얇은 입술", "도톰한 입술"]
# 얼굴 근처에 위치하는 스타일 (헤어/액세서리 등)
STYLES = ["덥수룩한 머리", "포니테일", "정갈한 가르마", "비니", "모자", "마스크 착용"]
# 얼굴에 붙어있는 눈에 띄는 점
SINGULARITIES = ["눈가 흉터", "입가 점", "뿔테 안경", "무선 이어폰", "피어싱"]

# 최대 단계 수 
MAX_LEVEL = 5
CRIME_TYPES = ["살인", "성폭력", "강도", "폭행", "상해"]

async def create_scenario(level: int) -> Scenario:
    if level <= 0 or level > MAX_LEVEL:
        raise TypeError("Levels must be from 1 to 5.")
    
    # 사건 정보 생성
    i_type = random.choice(CRIME_TYPES)
    i_place = random.choice(PLACES)
    i_timezone = random.choice(TIMEZONES)

    # 증인 생성
    is_female = random.choice([True, False])
    witness_name = namer.generate(False if is_female else True)
    witness_gender = "여성" if is_female else "남성"
    witness_personality = random.choice(PERSONALITIES)
    witness = Witness(witness_name, witness_gender, witness_personality)

    # 몽타주 생성
    composite_sketch = CompositeSketch()
    if level == 1:
        composite_sketch.set_face_shape(random.choice(FACE_SHAPES) if FACE_SHAPES else "")
    if level == 2:
        composite_sketch.set_eyes_of(random.choice(EYES_OFS) if EYES_OFS else "")
    if level == 3:
        composite_sketch.set_nose_and_mouth(random.choice(NOSE_AND_MOUTHS) if NOSE_AND_MOUTHS else "")
    if level == 4:
        composite_sketch.set_style(random.choice(STYLES) if STYLES else "")
    if level == 5:
        composite_sketch.set_singularity(random.choice(SINGULARITIES) if SINGULARITIES else "")

    # 시스템 프롬프트 생성
    ssp = create_statement_system_prompt(
        ct=i_type,
        name=witness.name,
        gender=witness.gender,
        place=i_place,
        timezone=i_timezone,
        per=witness.personality,
        cd=composite_sketch.cumulative_description
    )
    # 유저 프롬프트 생성
    scp = create_statement_user_prompt(name=witness.name)

    # 진술 생성
    raw_statement = await generate_content(scp, ssp)
    if not raw_statement:
        raise TypeError("statement is empty.")
    
    # 최종 시나리오 생성
    scenario = Scenario(
        witness=witness, 
        composite_sketch=composite_sketch,
        indicdent=i_type, 
        place=i_place, 
        timezone=i_timezone, 
        statement=raw_statement
    )

    return scenario