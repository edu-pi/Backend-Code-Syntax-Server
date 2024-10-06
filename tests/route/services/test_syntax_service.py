import os

import pytest

from app.route.execute.services import syntax_service

from app.web.exception.enum.error_enum import ErrorEnum
from app.web.exception.invalid_exception import InvalidSyntaxException


def test_check_fail(mocker):
    sample_code = "\na = 20\n"
    with mocker.patch('app.route.services.syntax_service._extract_syntax_error', return_value="Syntax error occurred."):
        with pytest.raises(InvalidSyntaxException) as exc:
            syntax_service.check(sample_code)

        # 예외가 발생했을 때, 결과 검증
        assert exc.value.result == {"error": "Syntax error occurred."}
        assert exc.value.error_enum == ErrorEnum.STATIC_SYNTAX_ERROR  # error_enum 확인


def test_check_success(mocker):
    sample_code = "\nprint(a)\n"
    with mocker.patch('app.route.services.syntax_service._extract_syntax_error', return_value=None):
        result = syntax_service.check(sample_code)

        assert result is True


def test__remove_indentation():
    code = """
            a = 20
            if a < 30:
                print("hello")
        """
    expected = '\na = 20\nif a < 30:\n    print("hello")\n'

    result = syntax_service._remove_indentation(code)

    assert result == expected


def test__create_temp_file_with_code():
    # 테스트할 코드 샘플
    sample_code = "print('Hello, World!')"

    temp_file_path = syntax_service._create_temp_file_with_code(sample_code)

    try:
        assert os.path.isfile(temp_file_path)

        # 파일 내용을 확인
        with open(temp_file_path, 'r') as temp_file:
            file_content = temp_file.read()
            assert file_content == sample_code
    finally:
        # 테스트 후 임시 파일 삭제
        if os.path.isfile(temp_file_path):
            os.remove(temp_file_path)


def test__run_flake8_fail():
    sample_code = '\nprint(a)\n'
    temp_file_path = syntax_service._create_temp_file_with_code(sample_code)

    result = syntax_service._run_flake8(temp_file_path)
    # 테스트 후 임시 파일 삭제
    if os.path.isfile(temp_file_path):
        os.remove(temp_file_path)

    print(result.stdout)
    assert result.returncode != 0


def test__run_flake8_success():
    sample_code = '\nprint("hello world")\n'
    temp_file_path = syntax_service._create_temp_file_with_code(sample_code)

    result = syntax_service._run_flake8(temp_file_path)
    # 테스트 후 임시 파일 삭제
    if os.path.isfile(temp_file_path):
        os.remove(temp_file_path)

    assert result.returncode == 0


def test__extract_error_message():
    origin = "/var/folders/0n/yb899qnj0vddx24q31c2t45h0000gn/T/tmpigduybq_.py:2:7: F821 undefined name 'a'"

    result = syntax_service._extract_error_message(origin)

    assert result == "2:7: F821 undefined name 'a'"


