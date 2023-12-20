import asyncio
import json
import pathlib

from model.user import User

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
persist_path = pathlib.Path(__file__).parent.absolute()


class UserFileRepository:
    def __init__(self):
        self.path = persist_path / "users.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = asyncio.Lock()

    async def _read_all(self) -> dict[str, User]:
        if not self.path.exists():
            return {}

        def read():
            with open(self.path, "r") as f:
                return json.load(f)

        data = await asyncio.to_thread(read)

        return {nickname: User(**user) for nickname, user in data.items()}

    async def _write_all(self, users: dict[str, User]) -> None:
        def write():
            with open(self.path, "w") as f:
                json.dump({nickname: user.__dict__ for nickname, user in users.items()}, f)

        await asyncio.to_thread(write)

    async def create(self, user: User) -> None:
        async with self.lock:
            users = await self._read_all()
            if user.nickname in users:
                raise ValueError(f"User {user.nickname} already exists")

            user.password = pwd_context.hash(user.password)
            users[user.nickname] = user
            await self._write_all(users)

    async def verify_password(self, nickname: str, password: str) -> bool:
        user = (await self._read_all()).get(nickname)
        if not user or not pwd_context.verify(password, user.password):
            return False
        return True

    async def get_all(self) -> list[User]:
        return list((await self._read_all()).values())
