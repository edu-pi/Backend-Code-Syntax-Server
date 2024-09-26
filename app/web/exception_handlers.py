from starlette import status

from app.route.services.exception.base_custom_exception import BaseCustomException
from app.route.services.exception.enum.error_enum import ErrorEnum
from app.route.services.exception.invalid_exception import InvalidException
from app.route.models.error_response import ErrorResponse

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidException)
    async def invalid_exception_handler(request: Request, exc: InvalidException):
        response = ErrorResponse(
            code=exc.error_enum.code,
            detail=exc.error_enum.detail,
            result=exc.result
        )
        return JSONResponse(
            status_code=exc.status,
            content=response.to_dict()
        )

    @app.exception_handler(BaseCustomException)
    async def base_exception_handler(request: Request, exc: BaseCustomException):
        response = ErrorResponse(
            code=exc.error_enum.code,
            detail=exc.error_enum.detail,
            result=exc.result
        )
        return JSONResponse(
            status_code=exc.status,
            content=response.to_dict()
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        response = ErrorResponse(
            code=ErrorEnum.UNKNOWN_ERROR.code,
            detail=ErrorEnum.UNKNOWN_ERROR.detail,
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.to_dict()
        )