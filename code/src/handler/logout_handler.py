import json

from model.user_state import AllUserInfos


async def quit_call_handler(remote_address: tuple[str, int]) -> None:
    # Verifica se o usuário está logado
    user = AllUserInfos.get_user(remote_address)
    if user is None:
        return

    # Avisa aos outros participantes da chamada que este usuário saiu da chamada
    for info in AllUserInfos.get_other_participants_same_topic(user):
        response = {
            "type": "quit_call",
            "success": True,
            "nickname": user.nickname,
        }
        await info.websocket.send(json.dumps(response))

    user.topic = None

    # Avisa aos outros usuários sobre o status deste usuário
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


async def logout_handler(remote_address: tuple[str, int]) -> None:
    # Sai da chamada, caso esteja em uma
    await quit_call_handler(remote_address)

    user = AllUserInfos.get_user(remote_address)
    if user is None:
        return

    # Avisa aos outros usuários que este usuário está offline
    for info in AllUserInfos.get_other_users(user):
        await info.websocket.send(
            json.dumps(
                {
                    "type": "user_status",
                    "users": [
                        {
                            "nickname": user.nickname,
                            "topic": user.topic,
                            "online": False,
                        }
                    ],
                }
            )
        )

    AllUserInfos.remove_user(remote_address)
