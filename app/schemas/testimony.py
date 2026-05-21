from pydantic import BaseModel


class TestimonyRequest(BaseModel):
    question: str
    case_name: str
    name: str
    reliability: int
    memory: str
    personality: str
    emotional_state: str = "calm"
    turn_count: int = 1


class TestimonyResponse(BaseModel):
    answer: str
    reliability_delta: int
    behavior_cue: str
    emotional_state: str
    inconsistency: bool
