import asyncio
import websockets
import json

connected_clients = set()

async def callback(websocket, path):
    print(f"New connection at {path}")
    connected_clients.add(websocket)
    try:
        async for packet in websocket:
            print("Packet Arrived")
            data = json.loads(packet)
            username = data.get("username")
            message = data.get("message")
            
            broadcast_message = json.dumps({"username": username, "message": message})
            #Passing coroutine objects to asyncio.wait() is deprecated since Python 3.8
            await asyncio.gather(*[client.send(broadcast_message) for client in connected_clients])
            print("Sent")
    except websockets.ConnectionClosed:
        print("Connection closed")
    finally:
        connected_clients.remove(websocket)
    
async def main():
    server = await websockets.serve(callback, "localhost", 8765, ping_interval=1000000)
    print("Server started on ws://localhost:8765")
    await server.wait_closed()
    
    
if __name__ == "__main__":
    asyncio.run(main())