import asyncio
import json

from handler.login_handler import login_handler
from handler.logout_handler import logout_handler, quit_call_handler
from handler.signup_handler import signup_handler
from handler.chat_handler import chat_handler
from handler.topic_handler import topic_handler
from handler.stream_handler import stream_handler

import websockets


async def main_handler(websocket: websockets.WebSocketServerProtocol):
    print(f"New connection from {websocket.remote_address}")
    while True:
        try:
            # Converte o JSON recebido em um dicionário
            data = json.loads(await websocket.recv())
            # Adiciona o websocket e o endereço remoto ao dicionário
            data["websocket"] = websocket
            data["remote_address"] = websocket.remote_address
            data_type = data.get("type", None)
            if data_type == "login":
                # Chama o handler de login
                await login_handler(data)
            elif data_type == "signup":
                # Chama o handler de cadastro de usuário
                await signup_handler(data)
            elif data_type == "chat":
                # Chama o handler de chat de texto
                await chat_handler(data)
            elif data_type == "topic":
                # Chama o handler de seleção de tópicos
                await topic_handler(data)
            elif data_type == "stream":
                # Chama o handler de stream de vídeo
                await stream_handler(data)
            elif data_type == "quit_call":
                # Chama o handler de saída de chamada
                await quit_call_handler(websocket.remote_address)
            else:
                # Caso o tipo de mensagem não seja reconhecido
                print(f"Unknown message type {data_type}")
                continue
        except websockets.exceptions.ConnectionClosed:
            # Caso a conexão seja fechada pelo cliente
            print(f"Connection closed from {websocket.remote_address}")
            await logout_handler(websocket.remote_address)
            break
        except json.JSONDecodeError:
            print("Invalid JSON")
        except Exception as e:
            print(f"Error: {e}")


async def main():
    host, port = "localhost", 8765
    print(f"Listening on ws://{host}:{port}")
    async with websockets.serve(main_handler, host, port):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
