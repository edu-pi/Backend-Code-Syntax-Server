import requests
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

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


class RequestCode(BaseModel):
    source_code: str


@app.post("/edupi_syntax/v1/python")
async def read_root(request_code: RequestCode):
    result = check_code(request_code.source_code)

    if result:
        return requests.post("http://localhost:8001/edupi_visualize/v1/python")
    else:
        return {"error": extract_error_message(result)}
