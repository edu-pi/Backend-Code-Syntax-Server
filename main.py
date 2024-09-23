import os.path
import requests

from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.responses import JSONResponse

from request_code import RequestCode
from syntax_checker import check_code, extract_error_message

load_dotenv()


class Settings:
    ENVIRONMENT = os.getenv('ENVIRONMENT')  # 환경 변수 ENVIRONMENT를 읽음
    ENGINE_SERVER = os.getenv(f'{ENVIRONMENT.upper()}_ENGINE_SERVER')


SWAGGER_HEADERS = {
    "title": "Code Syntax api",
    "version": "1.0.0",
}

app = FastAPI(
    swagger_ui_parameters={
        "deepLinking": True,
        "displayRequestDuration": True,
        "operationsSorter": "method",
        "filter": True,
        "tagsSorter": "alpha",
        "syntaxHighlight.theme": "tomorrow-night",
    },
    **SWAGGER_HEADERS
)


@app.get("/edupi_syntax")
def root():
    return JSONResponse(
        status_code=200,
        content="ok")


@app.post("/edupi_syntax/v1/check/static")
async def syntax_check(code: RequestCode):
    return_code, stdout = check_code(code.source_code)

    # 문법 오류가 있을 때
    if return_code != 0:
        return JSONResponse(
            status_code=400,
            content={"error": extract_error_message(stdout)}
        )

    # 시각화 분석 엔진에게 코드 분석 요청
    response = requests.post(
        Settings.ENGINE_SERVER,
        json={"source_code": code.source_code}
    )

    return JSONResponse(
        status_code=200,
        content=response.json()
    )
