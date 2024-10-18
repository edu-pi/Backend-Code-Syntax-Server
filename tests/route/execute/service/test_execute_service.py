import os

from app.route.execute.service import execute_service


def test__create_temp_file_with_code():
    # 테스트할 코드 샘플
    sample_code = "print('Hello, World!')"

    temp_file_path = execute_service._create_temp_file_with_code(sample_code)

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
    temp_file_path = execute_service._create_temp_file_with_code(sample_code)

    result = execute_service._run_flake8(temp_file_path)
    # 테스트 후 임시 파일 삭제
    if os.path.isfile(temp_file_path):
        os.remove(temp_file_path)

    print(result.stdout)
    assert result.returncode != 0


def test__run_flake8_success():
    sample_code = '\nprint("hello world")\n'
    temp_file_path = execute_service._create_temp_file_with_code(sample_code)

    result = execute_service._run_flake8(temp_file_path)
    # 테스트 후 임시 파일 삭제
    if os.path.isfile(temp_file_path):
        os.remove(temp_file_path)

    assert result.returncode == 0


def test__extract_error_message():
    origin = "/var/folders/0n/yb899qnj0vddx24q31c2t45h0000gn/T/tmpigduybq_.py:2:7: F821 undefined name 'a'"

    result = execute_service._extract_error_message(origin)

    assert result == "2:7: F821 undefined name 'a'"


