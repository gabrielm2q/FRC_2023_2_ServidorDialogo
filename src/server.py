import asyncio
import json

from handler.login_handler import login_handler
from handler.logout_handler import logout_handler
from handler.signup_handler import signup_handler

import websockets


async def main_handler(websocket: websockets.WebSocketServerProtocol):
    print(f"New connection from {websocket.remote_address}")
    while True:
        try:
            data = json.loads(await websocket.recv())
            data_type = data.pop("type", None)
            if data_type == "login":
                data["remote_address"] = websocket.remote_address
                response = await login_handler(data)
            elif data_type == "signup":
                response = await signup_handler(data)
            else:
                print("Unknown message type")
                continue

            await websocket.send(json.dumps({"type": data_type, **response}))
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection closed from {websocket.remote_address}")
            await logout_handler(websocket.remote_address)
            break
        except json.JSONDecodeError:
            # TODO: maybe send error message
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
