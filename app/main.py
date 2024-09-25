from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.exception import exception_handlers
from app.api.check import router as check_router

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

# Including routes from the routes.py file
app.include_router(check_router,  prefix="/edupi_syntax")
# 예외 핸들러를 app에 연결
exception_handlers.setup_exception_handlers(app)


@app.get("/edupi_syntax")
def root():
    return JSONResponse(
        status_code=200,
        content="ok")
