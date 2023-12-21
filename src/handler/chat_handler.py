import json
from typing import TypedDict

from model.user_state import AllUserInfos
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


# Interface para os dados recebidos pelo handler
class ChatData(TypedDict):
    type: str
    remote_address: tuple[str, int]
    message: str
    websocket: WebSocketServerProtocol


async def chat_handler(data: ChatData) -> None:
    # Verifica se o usuário está logado
    user = AllUserInfos.get_user(data["remote_address"])
    if user is None:
        response = HandlerResponse(
            type=data["type"], success=False, message="Usuário não está logado"
        )
        return await data["websocket"].send(json.dumps(response))

    # Verifica se o usuário está em algum tópico
    if user.topic is None:
        response = HandlerResponse(
            type=data["type"],
            success=False,
            message="Usuário não está em nenhum tópico",
        )
        return await data["websocket"].send(json.dumps(response))

    # Envia a mensagem para todos os outros participantes do tópico
    for info in AllUserInfos.get_other_participants_same_topic(user):
        response = HandlerResponse(
            type=data["type"],
            success=True,
            message=f"{user.nickname}: {data['message']}",
        )
        await info.websocket.send(json.dumps(response))

    # Envia a mensagem de volta para o usuário, formatada de acordo
    response = HandlerResponse(
        type=data["type"],
        success=True,
        message=f"Você: {data['message']}",
    )
    await user.websocket.send(json.dumps(response))
