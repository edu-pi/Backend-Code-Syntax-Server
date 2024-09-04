import requests
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from request_code import RequestCode
from syntax_checker import check_code, extract_error_message

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/edupi_syntax")
def root():
    return JSONResponse(status_code=200)


@app.post("/edupi_syntax/v1/python")
async def syntax_check(request_code: RequestCode):
    result = check_code(request_code.source_code)
    if result is True:
        # 시각화 분석 엔진에게 분석 요청
        response = requests.post(
            "http://localhost:8081/edupi_visualize/v1/python",
            json={"source_code": request_code.source_code}
        )
        return JSONResponse(
            status_code=200,
            content=response.json()
        )
    else:
        return JSONResponse(
            status_code=400,
            content={"error": extract_error_message(result)}
        )

