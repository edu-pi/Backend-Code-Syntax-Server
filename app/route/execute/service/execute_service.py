import os
import re
import subprocess
import tempfile
import textwrap

from RestrictedPython import compile_restricted, PrintCollector

from app.config.restricted_python_config import RestrictedPythonConfig
from app.route.execute.exception.code_execute_error import CodeExecuteError
from app.route.execute.exception.code_syntax_error import CodeSyntaxError
from app.web.exception.enum.error_enum import ErrorEnum


def execute_code(source_code: str, user_input: str):
    code = textwrap.dedent(source_code)
    input_values = user_input.split("\n")
    restricted_config = RestrictedPythonConfig(input_values)

    try:
        byte_code = compile_restricted(code, filename="<string>", mode="exec")
        restricted_locals = restricted_config.get_limited_locals()
        restricted_globals = restricted_config.get_limited_globals()

        exec(byte_code, restricted_globals, restricted_locals)

        return _get_print_result(restricted_locals)

    except SyntaxError as e:
        error = _get_error_message(source_code)
        raise CodeSyntaxError(ErrorEnum.CODE_SYNTAX_ERROR, {"error": error} if e.args else {})

    except Exception as e:
        error = _get_error_message(source_code)
        raise CodeExecuteError(ErrorEnum.CODE_EXEC_ERROR, {"error": error, "message": e.args[0]} if e.args else {})


def _get_print_result(restricted_locals):
    """_print 변수가 존재할 경우, 그 결과 반환."""
    if "_print" in restricted_locals:
        if isinstance(restricted_locals["_print"], PrintCollector):
            return "".join(restricted_locals["_print"].txt)  # 리스트 요소를 합쳐 하나의 문자열로

    return ""


def _get_error_message(code):
    """ 잘못된 코드의 에러 메시지를 추출 ex)'1:26: E999 SyntaxError: '(' was never closed' """
    code = textwrap.dedent(code)
    temp_file_path = _create_temp_file_with_code(code)

    result = _run_flake8(temp_file_path)
    os.remove(temp_file_path)

    if result.returncode != 0:
        return _extract_error_message(result.stdout)

    return None


def _create_temp_file_with_code(code) -> str:
    """ 임시 파일에 코드 저장후, 파일 경로 반환 """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        return temp_file.name


def _run_flake8(temp_file_path: str) -> subprocess.CompletedProcess:
    """ Flake8을 실행하여 코드 검사 """
    result = subprocess.run(
        ['flake8', temp_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result


def _extract_error_message(error_string) -> str:
    # [행:열: error message] 형태로 추출
    pattern = r"(\d+:\d+: [^\n]+)"

    # 정규 표현식을 사용하여 매칭된 부분 추출
    match = re.search(pattern, error_string)

    if match:
        return match.group(1)  # 매칭된 부분을 반환
    else:
        return "No match found."
