from fastapi import Form
from pydantic import BaseModel
from typing import List, Tuple

class GeneralRequest(BaseModel):
    client_id: str

    @classmethod
    def as_form(cls, client_id: str = Form(...)):
        return cls(client_id=client_id)

class GeneralResponse(BaseModel):
    message: str

class RetrieveScenarioRequest(BaseModel):
    client_id: str
    level: int

class RetrieveScenarioResponse(BaseModel):
    name: str
    gender: str
    statement: str

class UploadMontageResponse(BaseModel):
    details: List[Tuple[str, int, float]]
    total_score: int