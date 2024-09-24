class ErrorResponse:
    def __init__(self, code: str, detail_message: str, result: list = None):
        self.code = code
        self.detail_message = detail_message
        self.result = result if result is not None else []

    def to_dict(self):
        # Convert the response object to a dictionary
        return {
            "code": self.code,
            "detail_message": self.detail_message,
            "result": self.result,
        }