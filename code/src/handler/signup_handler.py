import json
from typing import TypedDict

from model.user import User
from database.user_file_repository import UserFileRepository
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


class SignupData(TypedDict):
    type: str
    nickname: str
    password: str
    websocket: WebSocketServerProtocol


async def signup_handler(data: SignupData) -> None:
    user = User(data["nickname"], data["password"])
    try:
        repository = UserFileRepository()
        await repository.create(user)
        response = HandlerResponse(
            type=data["type"], success=True, message="Usuário criado com sucesso"
        )
    except Exception:
        response = HandlerResponse(
            type=data["type"], success=False, message="Usuário com esse nome já existe"
        )

    await data["websocket"].send(json.dumps(response))
