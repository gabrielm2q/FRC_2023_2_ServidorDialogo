from dataclasses import dataclass

from websockets import WebSocketServerProtocol


@dataclass(slots=True)
class UserInfo:
    nickname: str
    websocket: WebSocketServerProtocol
    topic: str | None = None


class AllUserInfos:
    _remote_addresses: dict[tuple[str, int], UserInfo] = {}
    _topics: dict[str, tuple[str, int]]

    @classmethod
    def add_user(cls, address: tuple[str, int], info: UserInfo) -> None:
        cls._remote_addresses[address] = info

    @classmethod
    def remove_user(cls, address: tuple[str, int]) -> None:
        cls._remote_addresses.pop(address, None)

    @classmethod
    def get_user(cls, address: tuple[str, int]) -> UserInfo | None:
        return cls._remote_addresses.get(address, None)

    @classmethod
    def get_other_participants(cls, user: UserInfo | None) -> list[UserInfo]:
        if not user or not user.topic:
            return []
        return [
            info
            for info in cls._remote_addresses.values()
            if info.topic == user.topic and info != user
        ]
