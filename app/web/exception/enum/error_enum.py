from enum import Enum


class ErrorEnum(Enum):

    # 400
    TASK_FAIL = "CS-400001", "There is a problem with the service login"
    CODE_SYNTAX_ERROR = "CS-400002", "The code is incorrect syntax"
    CODE_CORRECT_FAIL = ("CS-400003", "code correct fail")
    UNKNOWN_ERROR = ("CS-400999", "The unexpected error")


    CODE_EXEC_ERROR = "CS-400004", "The format is not supported for security reasons"
    INPUT_SIZE_MATCHING_ERROR = "CS-400005", "The number of user inputs does not match."
    CODE_VISUALIZE_ERROR = "CS-400006", "아직 시각화할 수 없는 문법이 포함되어 있습니다."

    #500
    OPENAI_SERVER_ERROR = ("CS-504001", "Open AI internal server error")
    OPENAI_MAX_TOKEN_LIMIT = ("CS-504002", "Open AI max token limit")

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

    def to_dict(self):
        return {
            "code": self.code,
            "detail": self.detail,
        }
