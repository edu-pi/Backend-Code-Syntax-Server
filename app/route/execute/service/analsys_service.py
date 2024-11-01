import requests
from app.config.settings import Settings


def analyze_code(source_code: str, user_input: str):
    visualise_url = "/".join([Settings.ENGINE_SERVER, "v1", "python"])
    success_response = requests.post(
        visualise_url,
        json={"source_code": source_code, "input": user_input}
    )
    return success_response.json().get("result").get("code")

