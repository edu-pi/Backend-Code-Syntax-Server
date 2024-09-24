from pydantic import BaseModel


class RequestCode(BaseModel):
    source_code: str