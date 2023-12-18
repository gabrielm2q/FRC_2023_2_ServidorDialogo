import json
from typing import TypedDict

from model.user_state import AllUserInfos
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


class TopicData(TypedDict):
    type: str
    remote_address: tuple[str, int]
    websocket: WebSocketServerProtocol
    topic: str | None


async def topic_handler(data: TopicData) -> None:
    user = AllUserInfos.get_user(data["remote_address"])
    if user is None:
        response = HandlerResponse(
            type=data["type"], success=False, message="Usuário não está logado"
        )
        return await data["websocket"].send(json.dumps(response))

    user.topic = data["topic"]
    AllUserInfos.add_user(data["remote_address"], user)
    response = HandlerResponse(
        type=data["type"], success=True, message=f"Entrou no tópico {data['topic']}"
    )
    await data["websocket"].send(json.dumps(response))
