from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.web import exception_handlers
from app.route.check import router as check_router
from app.web.logger import log_request, log_response

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

# 미들웨어 등록
app.middleware("http")(log_request)
app.middleware("http")(log_response)

# 라우터 등록
app.include_router(check_router,  prefix="/edupi-syntax")

# 핸들러 등록
exception_handlers.setup_exception_handlers(app)


@app.get("/edupi-syntax", response_class=JSONResponse)
def root():
    return JSONResponse(
        status_code=200,
        content="ok")
