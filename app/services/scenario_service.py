from app.enums import MAX_LEVEL, CrimeType, Place, TimeZone, random_enum
from app.models import Scenario, build_composite_sketch, build_witness
from app.utils.prompt_templates import create_statement_system_prompt, create_statement_user_prompt
from app.services.llm_client import generate_content

async def create_scenario(level: int) -> Scenario:
    if not (1 <= level <= MAX_LEVEL):
        raise ValueError(f"The level must be at least 1 and not more than {MAX_LEVEL}. (Received value: {level})")

    crime_type = random_enum(CrimeType)
    place = random_enum(Place)
    timezone = random_enum(TimeZone)

    witness = build_witness()
    composite_sketch = build_composite_sketch(level)

    system_prompt = create_statement_system_prompt(
        ct=crime_type,
        name=witness.name,
        gender=witness.gender,
        place=place,
        timezone=timezone,
        per=witness.personality,
        cd=composite_sketch.cumulative_description,
    )
    user_prompt = create_statement_user_prompt(name=witness.name)

    raw_statement = await generate_content(user_prompt, system_prompt)
    if not raw_statement:
        raise ValueError("LLM returned an empty statement.")

    return Scenario(
        witness=witness,
        composite_sketch=composite_sketch,
        crime_type=crime_type,
        place=place,
        timezone=timezone,
        statement=raw_statement,
    )