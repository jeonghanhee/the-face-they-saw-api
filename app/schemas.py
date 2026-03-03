from pydantic import BaseModel
from typing import Dict

class GeneralRequest(BaseModel):
    client_id: str

class GeneralResponse(BaseModel):
    message: str

class RetrieveScenarioRequest(BaseModel):
    client_id: str
    level: int

class RetrieveScenarioResponse(BaseModel):
    name: str
    gender: str
    statement: str