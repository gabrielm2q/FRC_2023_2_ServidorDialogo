import json
from typing import TypedDict

from model.user import User
from database.user_file_repository import UserFileRepository
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


# Interface para os dados recebidos pelo handler
class SignupData(TypedDict):
    type: str
    nickname: str
    password: str
    websocket: WebSocketServerProtocol


async def signup_handler(data: SignupData) -> None:
    user = User(data["nickname"], data["password"])
    try:
        # Adiciona o usuário ao "banco de dados"
        repository = UserFileRepository()
        await repository.create(user)
        response = HandlerResponse(
            type=data["type"], success=True, message="Usuário criado com sucesso"
        )
    except Exception:
        response = HandlerResponse(
            type=data["type"], success=False, message="Usuário com esse nome já existe"
        )

    # Envia a mensagem de sucesso de volta para o usuário
    await data["websocket"].send(json.dumps(response))
