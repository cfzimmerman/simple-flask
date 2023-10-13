from typing import TypedDict, Any


class ErrorResponse(TypedDict):
    code: int
    message: str


class SuccessResponse(TypedDict):
    code: int
    data: Any


class PostColor(TypedDict):
    user_uuid: str
    color: str


class GetColor(TypedDict):
    user_uuid: str
