import json
from typing import TypedDict

from database.user_file_repository import UserFileRepository
from model.user_state import AllUserInfos, UserInfo
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


class LoginData(TypedDict):
    type: str
    nickname: str
    password: str
    remote_address: tuple[str, int]
    websocket: WebSocketServerProtocol


async def login_handler(data: LoginData) -> None:
    repository = UserFileRepository()
    if await repository.verify_password(data["nickname"], data["password"]):
        AllUserInfos.add_user(
            data["remote_address"],
            UserInfo(
                nickname=data["nickname"],
                websocket=data["websocket"],
                topic="General",
            ),
        )

        response = HandlerResponse(
            type=data["type"], success=True, message="Login realizado com sucesso"
        )
    else:
        response = HandlerResponse(
            type=data["type"], success=False, message="Usuário ou senha incorretos"
        )

    await data["websocket"].send(json.dumps(response))
