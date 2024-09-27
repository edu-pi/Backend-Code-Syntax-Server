from pydantic import BaseModel


class Step(BaseModel):
    row: int
    correct: str


class CorrectResponse(BaseModel):
    reason: str
    steps: list[Step]
