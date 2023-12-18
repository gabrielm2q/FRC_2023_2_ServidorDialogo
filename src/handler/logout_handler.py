from model.user_state import UserStateRepository
from handler import HandlerResponse


async def logout_handler(remote_address: tuple[str, int]) -> HandlerResponse:
    UserStateRepository.set_offline(remote_address)

    return HandlerResponse(
        {
            "success": True,
            "message": "Logout efetuado com sucesso",
            "data": None,
        }
    )
