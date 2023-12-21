from typing import TypedDict


# Interface para o retorno dos handlers
class HandlerResponse(TypedDict):
    type: str
    message: str
    success: bool
