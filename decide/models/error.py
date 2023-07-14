from typing import Any

class DecideException(Exception):
    def __init__(self, message, status_code=None, endpoint=None, request_payload=None, response_headers=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.endpoint = endpoint
        self.request_payload = request_payload
        self.response_headers = response_headers

    def __str__(self):
        additional_info_str = ', '.join(f"{key}={value}" for key, value in self.__dict__.items() if value is not None and key != 'message')
        return f"Decide Exception: {self.message}. Additional info: {additional_info_str}"


class IllegalAssignmentException(DecideException):
    """When the user tries to illegally change the value of a private field"""
