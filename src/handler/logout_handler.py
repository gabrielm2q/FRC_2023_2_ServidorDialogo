import json

from model.user_state import AllUserInfos


async def quit_call_handler(remote_address: tuple[str, int]) -> None:
    user = AllUserInfos.get_user(remote_address)
    if user is None:
        return

    for info in AllUserInfos.get_other_participants_same_topic(user):
        response = {
            "type": "quit_call",
            "success": True,
            "nickname": user.nickname,
        }
        await info.websocket.send(json.dumps(response))

    user.topic = None

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
    await quit_call_handler(remote_address)

    user = AllUserInfos.get_user(remote_address)
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
                            "online": False,
                        }
                    ],
                }
            )
        )

    AllUserInfos.remove_user(remote_address)
