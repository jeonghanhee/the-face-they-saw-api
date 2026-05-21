from fastapi import Form
from pydantic import BaseModel
from typing import List


class PortraitItem(BaseModel):
    name: str
    score: int


class PortraitRequest(BaseModel):
    criteria: List[str]

    @classmethod
    def as_form(cls, criteria: List[str] = Form(...)):
        return cls(criteria=criteria)


class PortraitResponse(BaseModel):
    details: List[PortraitItem]
    score: int
