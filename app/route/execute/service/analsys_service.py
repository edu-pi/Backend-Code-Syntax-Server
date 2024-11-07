import requests
from app.config.settings import Settings
from app.route.execute.exception.code_visualize_error import CodeVisualizeError
from app.web.exception.enum.error_enum import ErrorEnum


def analyze_code(source_code: str, user_input: str):
    visualise_url = "/".join([Settings.ENGINE_SERVER, "v1", "python"])
    response = requests.post(
        visualise_url,
        json={"source_code": source_code, "input": user_input}
    )
    if not response.ok:
        raise CodeVisualizeError(ErrorEnum.CODE_VISUALIZE_ERROR)

    return response.json().get("result").get("code")
