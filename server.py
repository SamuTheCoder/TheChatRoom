import asyncio
import websockets
import json
from database import *

connected_clients = {}

async def callback(websocket, path):
    print(f"New connection at {path}")    
    
    await send_previous_messages(websocket)
    
    temp = 0
    
    try:
        async for packet in websocket:
            data = json.loads(packet)
            print(f"Packet Arrived: {data}")
            username = data.get("username")
            message = data.get("message")
            
            if temp == 0:
                if not create_session(username):
                    await websocket.send(json.dumps({"error": "There's a session with this username already established"}))
                    await websocket.close()
                    break
            
                temp += 1
                connected_clients[websocket] = username
                create_session(username)
                
            user_id = create_user(username)
            create_message(user_id, username, message)
            
            await broadcast_message(username, message)
            
    except websockets.ConnectionClosed:
        print("Connection closed")
    finally:
        if websocket in connected_clients:
            end_session(username)
            connected_clients.pop(websocket)

async def send_previous_messages(websocket):
    last_messages = get_history()
    
    for message in reversed(last_messages):
        broadcast_message = json.dumps({
            "username": message["username"],
            "message": message["message"]
        })
        
        await websocket.send(broadcast_message)
        
async def broadcast_message(username, message):
    broadcast_message = json.dumps({"username": username, "message": message})
    #Passing coroutine objects to asyncio.wait() is deprecated since Python 3.8
    await asyncio.gather(*[client.send(broadcast_message) for client in connected_clients])
    print("Sent")
    
async def main():
    sessions = sessions_collection.find()
        
    for session in sessions:
        print("Session Document: ")
        for key in session:
            value = session[key]
            print(f"{key}: {value}\n")
    server = await websockets.serve(callback, "localhost", 8765, ping_interval=10, ping_timeout=10)
    print("Server started on ws://localhost:8765")
    await server.wait_closed()
    
    
if __name__ == "__main__":
    asyncio.run(main())