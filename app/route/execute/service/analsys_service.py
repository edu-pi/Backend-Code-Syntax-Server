# app/services/analysis_service.py
import requests
from app.config.settings import Settings


def analyze_code(source_code: str, input: str):
    url = "/".join([Settings.ENGINE_SERVER, "v1", "python"])
    success_response = requests.post(
        url,
        json={"source_code": source_code}
    )
    return success_response

