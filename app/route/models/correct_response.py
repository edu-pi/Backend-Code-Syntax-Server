from pydantic import BaseModel


class ModifiedCode(BaseModel):
    line: int
    code: str


class CorrectResponse(BaseModel):
    reason: str
    modified_codes: list[ModifiedCode]
