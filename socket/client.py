import websockets
import asyncio

async def listen():
    """
    Connect to the server and then handle whatever comes back from the server.
    """
    url = "ws://localhost:7890"  # Changed from 127.0.0.1 to localhost to match server

    try:
        async with websockets.connect(url) as websocket:
            await websocket.send("Hello from the other side!!!")
            while True:
                msg = await websocket.recv()
                print(f"msg: {msg}")
    except websockets.exceptions.ConnectionClosed:
        print("Connection with server closed")
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure server is running.")

async def main():
    await listen()

if __name__ == "__main__":
    asyncio.run(main())