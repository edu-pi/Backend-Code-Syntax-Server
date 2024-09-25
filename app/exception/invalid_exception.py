from starlette import status

from app.exception.base_custom_exception import BaseCustomException
from app.exception.custom_error import CustomError


class InvalidException(BaseCustomException):
    def __init__(self, custom_error: CustomError, result: dict):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            custom_error=custom_error,
            result={} if result is None else result
        )


