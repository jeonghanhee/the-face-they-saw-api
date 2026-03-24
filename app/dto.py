from fastapi import Form
from pydantic import BaseModel
from typing import List, Optional, Tuple

class InvestigateRequest(BaseModel):
    question: str
    case_name: str
    name: str
    reliability: int
    memory: str
    personality: str

class InvestigateResponse(BaseModel):
    answer: str
    reliability_delta: int

class UploadRequest(BaseModel):
    criteria: List[str]

    @classmethod
    def as_form(cls, criteria: List[str] = Form(...)):
        return cls(criteria=criteria)

class ScoredItem(BaseModel):
    name: str
    score: int

class UploadResponse(BaseModel):
    details: List[ScoredItem]
    score: int