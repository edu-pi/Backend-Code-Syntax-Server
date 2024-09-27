from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.route.models.correct_request import CorrectRequest
from app.route.models.correct_response import CorrectResponse
from app.route.models.success_reponse import SuccessResponse

router = APIRouter()


@router.post("/v1/correct")
async def syntax_check(correct_request: CorrectRequest):
    correct_response = CorrectResponse(row=1, correct="a = 10")

    success_response = SuccessResponse(
        detail="success correct",
        result=correct_response.dict()
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )
