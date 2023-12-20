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
    if not await repository.verify_password(data["nickname"], data["password"]):
        response = HandlerResponse(
            type=data["type"], success=False, message="Usuário ou senha incorretos"
        )
        return await data["websocket"].send(json.dumps(response))

    AllUserInfos.add_user(
        data["remote_address"],
        UserInfo(
            nickname=data["nickname"],
            websocket=data["websocket"],
            topic=None,
        ),
    )

    response = HandlerResponse(
        type=data["type"], success=True, message="Login realizado com sucesso"
    )
    await data["websocket"].send(json.dumps(response))

    user = AllUserInfos.get_user(data["remote_address"])
    if user is None:
        return

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

    users = [
        {
            "nickname": info.nickname,
            "topic": info.topic,
            "online": True,
        }
        for info in AllUserInfos.get_other_users(user)
    ]
    online_users = {info.nickname for info in AllUserInfos.get_other_users(user)}
    online_users.add(user.nickname)
    users.extend(
        [
            {
                "nickname": x.nickname,
                "topic": None,
                "online": False,
            }
            for x in await repository.get_all()
            if x.nickname not in online_users
        ]
    )
    await data["websocket"].send(
        json.dumps(
            {
                "type": "user_status",
                "users": users,
            }
        )
    )
