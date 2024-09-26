from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.route.models.success_reponse import SuccessResponse
from app.route.models.code_request import CodeRequest
from app.route.services import syntax_service
from app.route.services import analsys_service

router = APIRouter()


@router.post("/check/v1/static")
async def syntax_check(code: CodeRequest):
    # 문법 체크
    syntax_service.check(code.source_code)
    # 코드 분석
    analysis_result = analsys_service.analyze_code(code.source_code)

    success_response = SuccessResponse(
        detail="success code analysis",
        result={"code": analysis_result.json()}
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )
