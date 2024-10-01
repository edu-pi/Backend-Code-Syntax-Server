from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.route.models.code_request import CodeRequest
from app.route.models.success_reponse import SuccessResponse
from app.route.services import ai_service

router = APIRouter()


@router.post("/v1/advice/correct")
async def syntax_check(code_request: CodeRequest):
    correct_response = await ai_service.correct(code=code_request.source_code)

    success_response = SuccessResponse(
        detail="success correct",
        result=correct_response.dict()
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )
