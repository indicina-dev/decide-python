from typing import Any


class DecideException(Exception):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        extra = ""
        if args:
            extra = f"\n| extra info: {args[0]}"
        print(f"[{self.__class__.__name__}]: {self.__doc__}{extra}")
        Exception.__init__(self, *args)


class IllegalAssignmentException(DecideException):
    """When the user tries to illegally change the value of a private field"""
