import asyncio
import json
import pathlib

from model.user import User

from passlib.context import CryptContext

# Define o algoritmo de criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Define o caminho para o arquivo de persistência de usuários
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

        # Lê o arquivo em uma thread separada
        data = await asyncio.to_thread(read)

        # Converte o dicionário de dicionários em um dicionário de usuários
        return {nickname: User(**user) for nickname, user in data.items()}

    async def _write_all(self, users: dict[str, User]) -> None:
        def write():
            with open(self.path, "w") as f:
                json.dump({nickname: user.__dict__ for nickname, user in users.items()}, f)

        # Escreve o arquivo em uma thread separada
        await asyncio.to_thread(write)

    async def create(self, user: User) -> None:
        # Garante que apenas uma thread escreva no arquivo por vez
        async with self.lock:
            # Lê todos os usuários
            users = await self._read_all()
            # Verifica se o usuário já existe
            if user.nickname in users:
                raise ValueError(f"User {user.nickname} already exists")

            # Criptografa a senha
            user.password = pwd_context.hash(user.password)
            # Adiciona o usuário ao dicionário
            users[user.nickname] = user
            # Escreve o dicionário de volta no arquivo
            await self._write_all(users)

    async def verify_password(self, nickname: str, password: str) -> bool:
        user = (await self._read_all()).get(nickname)
        # Verifica se o usuário existe e se a senha está correta
        if not user or not pwd_context.verify(password, user.password):
            return False
        return True

    async def get_all(self) -> list[User]:
        # Retorna uma lista com todos os usuários
        return list((await self._read_all()).values())
