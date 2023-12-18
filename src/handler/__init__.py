from typing import TypedDict


class HandlerResponse(TypedDict):
    type: str
    message: str
    success: bool
