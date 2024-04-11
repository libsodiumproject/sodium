class HttpError(Exception):
    def __init__(self, code: int, message: str):
        self.message = message
        self.code = code
