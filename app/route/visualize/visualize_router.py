from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.web.models.success_reponse import SuccessResponse
from app.route.visualize.models.code_request import CodeRequest
from app.route.visualize import analsys_service, syntax_service

visualize_router = APIRouter()


@visualize_router.post("/v1/visualize")
async def visualize(code: CodeRequest):
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
