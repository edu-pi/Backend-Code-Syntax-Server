from app.exception.custom_error import CustomError


class BaseCustomException(Exception):
    def __init__(self, status_code: int, custom_error: CustomError, result: dict):
        self.status_code = status_code
        self.custom_error = custom_error
        self.result = [] if result is None else result
