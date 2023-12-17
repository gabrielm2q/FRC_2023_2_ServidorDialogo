from enum import Enum, auto


class UserState(Enum):
    ONLINE = auto()
    BUSY = auto()
    OFFLINE = auto()


class UserStateRepository:
    users: dict[str, UserState] = {}
    remote_addresses: dict[tuple[str, int], str] = {}

    @classmethod
    def set_state(
        cls, nickname: str, address: tuple[str, int], state: UserState
    ) -> None:
        cls.remote_addresses[address] = nickname
        cls.users[nickname] = state

    @classmethod
    def set_offline(cls, address: tuple[str, int]) -> None:
        nickname = cls.remote_addresses.pop(address, "")
        cls.users.pop(nickname, None)

    @classmethod
    def get_state_by_nickname(cls, nickname: str) -> UserState:
        return cls.users.get(nickname, UserState.OFFLINE)

    @classmethod
    def get_state_by_address(cls, address: tuple[str, int]) -> UserState:
        return cls.get_state_by_nickname(cls.remote_addresses.get(address, ""))
