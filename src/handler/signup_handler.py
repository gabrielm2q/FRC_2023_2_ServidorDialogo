from typing import TypedDict

from model.user import User
from database.user_file_repository import UserFileRepository
from handler import HandlerResponse


class SignupData(TypedDict):
    nickname: str
    password: str


async def signup_handler(data: SignupData) -> HandlerResponse:
    user = User(data["nickname"], data["password"])
    try:
        repository = UserFileRepository()
        await repository.create(user)
        return HandlerResponse(
            {
                "success": True,
                "message": "Usuário criado com sucesso",
                "data": None,
            }
        )
    except Exception:
        return HandlerResponse(
            {
                "success": False,
                "message": "Usuário já existe",
                "data": None,
            }
        )
