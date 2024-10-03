# app/services/analysis_service.py
import requests
from app.config.settings import Settings


def analyze_code(source_code: str):
    response = requests.post(
        Settings.ENGINE_SERVER,
        json={"source_code": source_code}
    )
    return response
