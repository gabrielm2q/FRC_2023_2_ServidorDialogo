import json

from model.user_state import AllUserInfos
from handler import HandlerResponse


async def logout_handler(remote_address: tuple[str, int]) -> None:
    user = AllUserInfos.get_user(remote_address)
    if user is None:
        return
    for info in AllUserInfos.get_other_participants(user):
        response = HandlerResponse(
            type="chat",
            success=True,
            message=f"{user.nickname} saiu da chamada",
        )
        await info.websocket.send(json.dumps(response))
    AllUserInfos.remove_user(remote_address)
