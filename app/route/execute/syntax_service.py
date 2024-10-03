import os
import re
import subprocess
import tempfile
import textwrap
from typing import Optional

from app.web.exception.enum.error_enum import ErrorEnum
from app.web.exception.invalid_exception import InvalidSyntaxException


def check(code):
    code = _remove_indentation(code)
    temp_file_path = _create_temp_file_with_code(code)

    result = _run_flake8(temp_file_path)

    os.remove(temp_file_path)

    syntax_error_message = _extract_syntax_error(result)
    if syntax_error_message:
        raise InvalidSyntaxException(
            error_enum=ErrorEnum.STATIC_SYNTAX_ERROR,
            result={"error": syntax_error_message}
        )

    return True


def _remove_indentation(code: str) -> str:
    """코드의 들여쓰기 제거"""
    return textwrap.dedent(code)


def _create_temp_file_with_code(code)-> str:
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


def _extract_syntax_error(result: subprocess.CompletedProcess) -> Optional[str]:
    """Flake8 결과에서 에러 메시지 추출"""
    if result.returncode != 0:
        return _extract_error_message(result.stdout)
    return None


def _extract_error_message(error_string)-> str:
    # [행:열: error message] 형태로 추출
    pattern = r"(\d+:\d+: [^\n]+)"

    # 정규 표현식을 사용하여 매칭된 부분 추출
    match = re.search(pattern, error_string)

    if match:
        return match.group(1)  # 매칭된 부분을 반환
    else:
        return "No match found."
