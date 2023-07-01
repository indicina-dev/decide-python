from typing import Any


class DecideException(Exception):
    def __init__(self, message, **kwargs):
        self.message = message
        self.additional_info = kwargs
    
    def __str__(self):
        if self.additional_info:
                additional_info_str = ', '.join(f"{key}={value}" for key, value in self.additional_info.items())
                return f"Decide Exception: {self.message}. Additional info: {additional_info_str}"
        else:
            return f"Decide Exception: {self.message}"


class IllegalAssignmentException(DecideException):
    """When the user tries to illegally change the value of a private field"""
