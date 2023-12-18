from typing import TypedDict

from database.user_file_repository import UserFileRepository
from model.user_state import UserState, UserStateRepository
from handler import HandlerResponse


class LoginData(TypedDict):
    nickname: str
    password: str
    remote_address: tuple[str, int]


async def login_handler(data: LoginData) -> HandlerResponse:
    repository = UserFileRepository()
    if await repository.verify_password(data["nickname"], data["password"]):
        UserStateRepository.set_state(
            data["nickname"], data["remote_address"], UserState.ONLINE
        )

        return HandlerResponse(
            {
                "success": True,
                "message": "Login efetuado com sucesso",
                "data": None,
            }
        )
    else:
        return HandlerResponse(
            {
                "success": False,
                "message": "Usuário ou senha incorretos",
                "data": None,
            }
        )
