from pydantic import BaseModel


class CorrectRequest(BaseModel):
    source_code: str