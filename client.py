import asyncio
import websockets
import json
            
async def send_message(websocket, username):
    while True:
        if websocket is None:
            print("Not connected to server")
            return
        try:
            message = input("Say something: ")
            packet = json.dumps({"username": username, "message": message})
            await websocket.send(packet)
        except Exception as e:
            print("Error: ", e)
        
async def recv_message(websocket):
    while True:
        if websocket is None:
            print("Not connected to server")
            return
        try:
            packet = await websocket.recv()
            response = json.loads(packet)
            username = response.get("username")
            message = response.get("message")
            print(f"{username}: {message}")
        except Exception as e:
            print("Error: ", e)
        
async def main(username):   
    uri = "ws://localhost:8765"
     
    async with websockets.connect(uri) as client:
        while True:
            send_task = asyncio.create_task(send_message(client, username))
            receive_task = asyncio.create_task(recv_message(client))
            await asyncio.gather(send_task, receive_task)
            
if __name__ == "__main__":
    print("Welcome to The Chat Room")
    username = input("Username: ")
    
    while True:
        asyncio.run(main(username))
            