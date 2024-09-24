from enum import Enum


class ErrorCode(Enum):
    STATIC_SYNTAX_ERROR = ("CS_400001", "코드 문법 오류입니다")

    def __init__(self, code, message):
        self.code = code
        self.message = message