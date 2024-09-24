from fastapi import FastAPI
from starlette.responses import JSONResponse

from routes import router


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
app.include_router(router)



@app.get("/edupi_syntax")
def root():
    return JSONResponse(
        status_code=200,
        content="ok")
