from typing import TypedDict, Any


class HandlerResponse(TypedDict):
    message: str
    success: bool
    data: Any
