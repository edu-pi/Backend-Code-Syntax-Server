from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.route.models.correct_request import CorrectRequest
from app.route.models.success_reponse import SuccessResponse
from app.route.services import ai_service

router = APIRouter()


@router.post("/v1/correct")
async def syntax_check(correct_request: CorrectRequest):
    correct_response = ai_service.correct(code=correct_request.source_code)

    success_response = SuccessResponse(
        detail="success correct",
        result=correct_response.dict()
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )
