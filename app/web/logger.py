from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
import logging

logger = logging.getLogger('uvicorn.logger')

if not logger.hasHandlers():
    logger.setLevel(logging.INFO)

    # 콘솔 핸들러 및 포맷 설정
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)


def get_logger():
    return logger


# Request 로깅 미들웨어
async def log_request(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    body = await request.body()
    logger.info(f"Request Body: {body.decode()}")
    response = await call_next(request)
    return response


# Response 로깅 미들웨어
async def log_response(request: Request, call_next):
    response = await call_next(request)

    # 응답 바디 로깅
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))

    logger.info(f"Response : {response.status_code} {response_body[0].decode()}")

    return response
