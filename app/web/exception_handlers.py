from openai import OpenAIError
from starlette import status
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.route.execute.exception.code_execute_error import CodeExecuteError
from app.route.execute.exception.code_syntax_error import CodeSyntaxError
from app.web.exception.base_exception import BaseCustomException
from app.web.exception.enum.error_enum import ErrorEnum
from app.web.exception.invalid_exception import InvalidException
from app.web.exception.openai_exception import OpenaiException
from app.web.models.error_response import ErrorResponse
from app.web.logger import logger


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

    @app.exception_handler(OpenaiException)
    async def openai_exception_handler(request: Request, exc: OpenaiException):
        logger.info(
            f"{exc.error_enum.code} - OpenAI exception occurred for URI: {request.url}.\n"
            f"          Error: {_get_unique_value_in_openAI_error(exc.result)}. "
        )

        response = ErrorResponse(
            code=ErrorEnum.TASK_FAIL.code,
            detail=ErrorEnum.TASK_FAIL.detail,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.to_dict()
        )

    @app.exception_handler(CodeExecuteError)
    async def code_execute_exception_handler(request: Request, exc: CodeExecuteError):
        response = ErrorResponse(code=exc.error_enum.code, detail=exc.error_enum.detail, result=exc.result)
        return JSONResponse(status_code=exc.status, content=response.to_dict())

    @app.exception_handler(CodeSyntaxError)
    async def code_execute_exception_handler(request: Request, exc: CodeSyntaxError):
        response = ErrorResponse(code=exc.error_enum.code, detail=exc.error_enum.detail, result=exc.result)
        return JSONResponse(status_code=exc.status, content=response.to_dict())

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
            result={}
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.to_dict()
        )

    def _get_unique_value_in_openAI_error(e: OpenAIError) -> dict:
        response = getattr(e, 'response', None)  # response가 없으면 None 반환
        status_code = response.status_code if response else "Unknown"  # response가 없으면 'Unknown'

        return {
            "error_type": type(e).__name__,  # 예외 클래스 이름
            "message": str(e),  # 예외 메시지
            "status_code": status_code  # 상태 코드
        }