import textwrap
from RestrictedPython import compile_restricted, PrintCollector
from app.route.execute.exception.code_execute_error import CodeExecuteError
from app.route.execute.exception.code_syntax_error import CodeSyntaxError
from app.route.execute.services.limit_env import LimitEnv
from app.web.exception.enum.error_enum import ErrorEnum


def execute_code(source_code: str, user_input: str):

    code = textwrap.dedent(source_code)
    input_values = user_input.split("\n")
    limit_env = LimitEnv(input_values)

    try:
        byte_code = compile_restricted(code, filename="<string>", mode="exec")
        restricted_locals = {}
        restricted_globals = limit_env.get_limited_globals()

        exec(byte_code, restricted_globals, restricted_locals)

        return get_print_result(restricted_locals)

    except SyntaxError as e:
        raise CodeSyntaxError(ErrorEnum.CODE_SYNTAX_ERROR, {"error": e.args} if e.args else {})

    except Exception as e:
        raise CodeExecuteError(ErrorEnum.CODE_EXEC_ERROR, {"error": e.args} if e.args else {})


def get_print_result(restricted_locals):
    """_print 변수가 존재할 경우, 그 결과 반환."""
    if "_print" in restricted_locals:
        if isinstance(restricted_locals["_print"], PrintCollector):
            return "".join(restricted_locals["_print"].txt)  # 리스트 요소를 합쳐 하나의 문자열로

    return ""


