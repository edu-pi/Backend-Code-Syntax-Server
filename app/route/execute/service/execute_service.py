import os
import re
import subprocess
import tempfile
import textwrap

from RestrictedPython import compile_restricted, PrintCollector

from app.route.execute.exception.code_execute_error import CodeExecuteError
from app.route.execute.exception.code_syntax_error import CodeSyntaxError
from app.web.exception.enum.error_enum import ErrorEnum

FORBIDDEN_IMPORTS = ["os", "sys", "subprocess", "shutil"]


def execute_code(source_code: str, user_input: str):
    if _contains_forbidden_imports(source_code):
        # 보안상 실행 안함
        raise CodeExecuteError(ErrorEnum.CODE_EXEC_ERROR)

    try:
        process = subprocess.run(
            args=["python3", "-c", source_code],
            input=user_input,
            capture_output=True,    # stdout, stderr 별도의 Pipe에서 처리
            timeout=3,  # limit child process execute time
            check=True,  # CalledProcessError exception if return_code is 0
            text=True
        )
        return process.stdout

    # 프로세스 실행 중 비정상 종료
    except subprocess.CalledProcessError as e:
        raise CodeSyntaxError(ErrorEnum.CODE_SYNTAX_ERROR, {"error": e.stderr})

    # 실행 시간 초과
    except subprocess.TimeoutExpired as e:
        raise CodeSyntaxError(ErrorEnum.TASK_FAIL)

    except Exception as e:
        error = _get_error_message(source_code)
        raise CodeExecuteError(ErrorEnum.CODE_EXEC_ERROR, {"error": error} if e.args else {})


def _contains_forbidden_imports(code: str) -> bool:
    # 금지된 모듈이 코드에 있는지 확인
    for module in FORBIDDEN_IMPORTS:
        if re.search(rf'\bimport\s+{module}\b', code):
            return True
    return False


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
