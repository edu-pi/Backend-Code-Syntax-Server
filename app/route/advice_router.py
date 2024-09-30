from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.route.models.code_request import CodeRequest
from app.route.models.hint_request import HintRequest
from app.route.models.success_reponse import SuccessResponse
from app.route.services import ai_service

advice_router = APIRouter()


@advice_router.post("/v1/advice/correct")
async def correct(code_request: CodeRequest):
    correct_response = await ai_service.correct(code=code_request.source_code)

    success_response = SuccessResponse(
        detail="success correct",
        result=correct_response.dict()
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )


@router.post("/v1/hint")
async def hint(hint_request: HintRequest):
    hint_response = await ai_service.hint(line=hint_request.line, code=hint_request.source_code)

    success_response = SuccessResponse(
        detail="success hint",
        result=hint_response.dict()
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )