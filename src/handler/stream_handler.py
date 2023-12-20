import json
from typing import TypedDict

from model.user_state import AllUserInfos
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


class StreamData(TypedDict):
    type: str
    remote_address: tuple[str, int]
    websocket: WebSocketServerProtocol
    data: str


async def stream_handler(data: StreamData) -> None:
    user = AllUserInfos.get_user(data["remote_address"])
    if user is None:
        response = HandlerResponse(
            type=data["type"], success=False, message="Usuário não está logado"
        )
        return await data["websocket"].send(json.dumps(response))

    if user.topic is None:
        response = HandlerResponse(
            type=data["type"],
            success=False,
            message="Usuário não está em nenhum tópico",
        )
        return await data["websocket"].send(json.dumps(response))

    for info in AllUserInfos.get_other_participants(user):
        response = {
            "success": True,
            "type": data["type"],
            "data": data["data"],
            "from": user.nickname,
        }
        await info.websocket.send(json.dumps(response))
