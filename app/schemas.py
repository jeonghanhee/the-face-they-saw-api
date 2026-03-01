from pydantic import BaseModel
from typing import Dict

class JoinRequest(BaseModel):
    client_id: str

class JoinResponse(BaseModel):
    message: str

class LeaveRequest(BaseModel):
    client_id: str

class LeaveResponse(BaseModel):
    message: str

class CreateScenarioRequest(BaseModel):
    client_id: str

class CreateScenarioResponse(BaseModel):
    name: str
    gender: str
    statement: str