from pydantic import BaseModel


class HintRequest(BaseModel):
    line: int
    source_code: str
