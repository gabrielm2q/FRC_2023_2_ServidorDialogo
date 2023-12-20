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

    for info in AllUserInfos.get_other_participants_same_topic(user):
        await info.websocket.send(
            json.dumps(
                {
                    "type": "enter_call",
                    "nickname": user.nickname,
                }
            )
        )

    for info in AllUserInfos.get_other_users(user):
        await info.websocket.send(
            json.dumps(
                {
                    "type": "user_status",
                    "users": [
                        {
                            "nickname": user.nickname,
                            "topic": user.topic,
                            "online": True,
                        }
                    ],
                }
            )
        )
