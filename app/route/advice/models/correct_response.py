from pydantic import BaseModel


class ModifiedCode(BaseModel):
    line: int
    code: str


class CorrectResponse(BaseModel):
    reason: str
    modified_codes: list[ModifiedCode]

    @classmethod
    async def of(cls, response_data: dict):
        modified_codes_data = response_data.get("modified_codes", [])
        modified_codes = [
            ModifiedCode(line=item.get("line", 0), code=item.get("code", ""))
            for item in modified_codes_data
        ]

        reason = response_data.get("reason", "틀린 원인을 찾을 수 없습니다.")

        return CorrectResponse(reason=reason, modified_codes= modified_codes)
