from enum import Enum


class CustomError(Enum):
    UNKNOWN_ERROR = ("CS_400000", "처리가 필요한 에러입니다.")
    STATIC_SYNTAX_ERROR = ("CS_400001", "코드 문법 오류입니다")

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail
