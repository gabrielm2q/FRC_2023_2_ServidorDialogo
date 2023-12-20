import json
from typing import TypedDict

from model.user_state import AllUserInfos
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


class ChatData(TypedDict):
    type: str
    remote_address: tuple[str, int]
    message: str
    websocket: WebSocketServerProtocol


async def chat_handler(data: ChatData) -> None:
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

    for info in AllUserInfos.get_other_participants_same_topic(user):
        response = HandlerResponse(
            type=data["type"],
            success=True,
            message=f"{user.nickname}: {data['message']}",
        )
        await info.websocket.send(json.dumps(response))

    response = HandlerResponse(
        type=data["type"],
        success=True,
        message=f"Você: {data['message']}",
    )
    await user.websocket.send(json.dumps(response))
