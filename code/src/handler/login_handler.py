import json
from typing import TypedDict

from database.user_file_repository import UserFileRepository
from model.user_state import AllUserInfos, UserInfo
from handler import HandlerResponse

from websockets import WebSocketServerProtocol


# Interface para os dados recebidos pelo handler
class LoginData(TypedDict):
    type: str
    nickname: str
    password: str
    remote_address: tuple[str, int]
    websocket: WebSocketServerProtocol


async def login_handler(data: LoginData) -> None:
    # Verifica se o usuário já está logado
    repository = UserFileRepository()
    if not await repository.verify_password(data["nickname"], data["password"]):
        response = HandlerResponse(
            type=data["type"], success=False, message="Usuário ou senha incorretos"
        )
        return await data["websocket"].send(json.dumps(response))

    # Adiciona o usuário ao estado global
    AllUserInfos.add_user(
        data["remote_address"],
        UserInfo(
            nickname=data["nickname"],
            websocket=data["websocket"],
            topic=None,
        ),
    )

    # Envia a mensagem de sucesso de volta para o usuário
    response = HandlerResponse(
        type=data["type"], success=True, message="Login realizado com sucesso"
    )
    await data["websocket"].send(json.dumps(response))

    user = AllUserInfos.get_user(data["remote_address"])
    if user is None:
        return

    # Avisa aos outros usuários que este usuário está online
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

    # Envia a lista de usuários para o usuário que acabou de logar
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
