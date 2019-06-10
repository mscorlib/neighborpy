from typing import Any


class ResponseModel(object):
    errors: int
    message: list
    data: Any

    def __init__(self, data, errors: int = 0, message: list = []):
        self.data = data
        self.errors = errors
        self.message = message
