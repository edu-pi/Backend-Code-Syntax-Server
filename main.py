import json
import requests

from fastapi import FastAPI
from starlette.responses import JSONResponse
from request_code import RequestCode
from syntax_checker import check_code, extract_error_message


# 설정 파일 로드
with open('config.json') as config_file:
    config = json.load(config_file)

# 환경 선택
environment = config['environment']
API_URL = config[environment]['API_URL']

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


@app.post("/edupi_syntax/v1/python")
async def syntax_check(request_code: RequestCode):
    return_code, stdout = check_code(request_code.source_code)

    # 문법 오류가 있을 때
    if return_code != 0:
        # 오류 내용과 함께 BAD_REQUEST 반환
        return JSONResponse(
            status_code=400,
            content={"error": extract_error_message(stdout)}
        )

    # 시각화 분석 엔진에게 코드 분석 요청
    response = requests.post(
        API_URL,
        json={"source_code": request_code.source_code}
    )
    return JSONResponse(
        status_code=200,
        content=response.json()
    )


