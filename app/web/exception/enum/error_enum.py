from enum import Enum


class ErrorEnum(Enum):

    # 400
    TASK_FAIL = "CS-400001", "잠시 후 다시 시도 해주세요"
    CODE_SYNTAX_ERROR = "CS-400002", "잘못된 문법입니다."
    CODE_CORRECT_FAIL = ("CS-400003", "코드 교정에 실패 했습니다.")
    UNKNOWN_ERROR = ("CS-400999", "처리가 필요한 에러입니다.")

    CODE_EXEC_ERROR = "CS-400004", "지원하지 않는 형식입니다."
    INPUT_SIZE_MATCHING_ERROR = "CS-400005", "입력한 개수가 일치하지 않습니다."


    #500
    OPENAI_SERVER_ERROR = ("CS-504001", "Open AI internal server error")
    OPENAI_MAX_TOKEN_LIMIT = ("CS-504002", "max token limit...")

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

    def to_dict(self):
        return {
            "code": self.code,
            "detail": self.detail,
        }
