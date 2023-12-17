import asyncio
import websockets


async def handler(websocket: websockets.WebSocketServerProtocol):
    while True:
        message = await websocket.recv()
        print(message)


async def main():
    host, port = "localhost", 8765
    print(f"Listening on ws://{host}:{port}")
    async with websockets.serve(handler, host, port):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
