import json
from typing import TypedDict

from model.user_state import AllUserInfos
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


# Interface para os dados recebidos pelo handler
class StreamData(TypedDict):
    type: str
    remote_address: tuple[str, int]
    websocket: WebSocketServerProtocol
    data: str


async def stream_handler(data: StreamData) -> None:
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

    # Envia o conteúdo do vídeo para todos os outros participantes do tópico
    for info in AllUserInfos.get_other_participants_same_topic(user):
        response = {
            "success": True,
            "type": data["type"],
            "data": data["data"],
            "from": user.nickname,
        }
        await info.websocket.send(json.dumps(response))
