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
    description: List[str]

    @classmethod
    def as_form(cls, description: List[str] = Form(...)):
        return cls(description=description)

class UploadResponse(BaseModel):
    details: List[Tuple[str, Optional[int]]]
    score: int