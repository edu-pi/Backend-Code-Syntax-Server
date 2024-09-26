from app.route.exception.enum.error_enum import ErrorEnum


class BaseCustomException(Exception):
    def __init__(self, error_enum: ErrorEnum, result: dict):
        self.error_enum = error_enum
        self.result = {} if result is None else result
