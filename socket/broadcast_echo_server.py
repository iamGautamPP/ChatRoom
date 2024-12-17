# here multiple clients can connect to the server and whatever message a client send to the server will be broadcasted to other clients

import websockets
import asyncio

PORT = 7890

connected = set() # to keep unique connected clients

async def echo(websocket):
    print(f"websocket: {websocket}")
    print("A Client just connected")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received a message from the client: {message}")
            for conn in connected:
                if conn != websocket:
                    await conn.send(f"Someone said : {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected.remove(websocket)

async def main():
    async with websockets.serve(echo, "localhost", PORT) as server:
        print(f"WebSocket server is running on ws://localhost:{PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())