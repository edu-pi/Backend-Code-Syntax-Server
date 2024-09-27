from pydantic import BaseModel


class CorrectRequest(BaseModel):
    row: int
    source_code: str
