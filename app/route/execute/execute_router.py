from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.web.models.success_reponse import SuccessResponse
from app.route.execute.models.code_request import CodeRequest
from app.route.execute.services import analsys_service, execute_service, syntax_service

execute_router = APIRouter()


@execute_router.post("/v1/execute/visualize")
async def visualize(code: CodeRequest):
    # 문법 체크
    code = syntax_service.check(code.source_code)
    # 코드 분석
    analysis_result = analsys_service.analyze_code(code)

    success_response = SuccessResponse(
        detail="success code analysis",
        result={"code": analysis_result.json()}
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )


@execute_router.post("/v1/execute/code")
async def execute(code_request: CodeRequest):
    # 코드 분석
    execute_result = execute_service.execute_code(code_request.source_code, code_request.input)

    success_response = SuccessResponse(
        detail="success execute",
        result={"output": execute_result}
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )
