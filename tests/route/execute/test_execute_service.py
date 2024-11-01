from app.route.execute.service.execute_service import _contains_forbidden_imports


def test__contains_forbidden_imports():
    code = "import os\n"

    assert _contains_forbidden_imports(code) is True
