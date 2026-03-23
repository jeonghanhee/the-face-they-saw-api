from fastapi import Form
from pydantic import BaseModel
from typing import List, Tuple

class InvestigateRequest(BaseModel):
    question: str
    trusLevel: int

class InvestigateResponse(BaseModel):
    answer: str
    trustDelta: int

class UploadRequest(BaseModel):
    description: List[str]

    @classmethod
    def as_form(cls, description: List[str] = Form(...)):
        return cls(description=description)

class UploadResponse(BaseModel):
    details: List[Tuple[str, int, float]]
    totalScore: int