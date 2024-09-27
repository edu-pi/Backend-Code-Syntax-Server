from pydantic import BaseModel


class CorrectResponse(BaseModel):
    row: int
    correct: str
