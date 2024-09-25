import requests
from fastapi import APIRouter
from starlette.responses import JSONResponse

from app._config.settings import Settings
from app.models.success_reponse import SuccessResponse
from app.models.code_request import CodeRequest
from app.api.services import syntax_checker

router = APIRouter()


@router.post("/check/v1/static")
async def syntax_check(code: CodeRequest):
    syntax_checker.check(code.source_code)

    # # 시각화 분석 엔진으로 코드 분석 요청
    analysis_result = requests.post(
        Settings.ENGINE_SERVER,
        json={"source_code": code.source_code}
    )

    success_response = SuccessResponse(
        detail="success code analysis",
        result={"code": analysis_result.json()}
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )
