from enum import Enum

from starlette.status import HTTP_400_BAD_REQUEST


class ErrorEnum(Enum):

    # 400
    STATIC_SYNTAX_ERROR = ("CS_400001", "코드 문법 오류입니다.")
    CODE_CORRECT_FAIL = ("CS_400002", "코드 교정에 실패 했습니다.")
    UNKNOWN_ERROR = ("CS_400999", "처리가 필요한 에러입니다.")

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail
