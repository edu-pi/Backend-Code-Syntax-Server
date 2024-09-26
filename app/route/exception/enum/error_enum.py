from enum import Enum

from starlette.status import HTTP_400_BAD_REQUEST


class ErrorEnum(Enum):

    # 400
    STATIC_SYNTAX_ERROR = (HTTP_400_BAD_REQUEST, "CS_400001", "코드 문법 오류입니다")
    UNKNOWN_ERROR = (HTTP_400_BAD_REQUEST, "CS_400999", "처리가 필요한 에러입니다.")

    def __init__(self, status, code, detail):
        self.status = status
        self.code = code
        self.detail = detail
