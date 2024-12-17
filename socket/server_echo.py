import websockets
import asyncio

PORT = 7890

async def echo(websocket):
    print("A Client just connected")
    try:
        async for message in websocket:
            print(f"Received a message from the client: {message}")
            await websocket.send(f"response message: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(echo, "localhost", PORT) as server:
        print(f"WebSocket server is running on ws://localhost:{PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())