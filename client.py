import asyncio
import websockets
import json
import aioconsole
            
async def send_message(websocket, username):
    while True:
        if websocket is None:
            print("Not connected to server")
            return
        try:
            message = await aioconsole.ainput("")
            packet = json.dumps({"username": username, "message": message})
            await websocket.send(packet)
        except Exception as e:
            print("Error: ", e)
            break
        
async def recv_message(websocket):
    while True:
        if websocket is None:
            print("Not connected to server")
            return
        try:
            packet = await websocket.recv()
            response = json.loads(packet)
            if "error" in response:
                print(f"Error: {response['error']}")
                break
            username = response.get("username")
            message = response.get("message")
            print(f"{username}: {message}")
        except Exception as e:
            print("Error: ", e)
            break
          
async def main(username):   
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as client:
            send_task = asyncio.create_task(send_message(client, username))
            receive_task = asyncio.create_task(recv_message(client))
            
            try:
                await asyncio.gather(send_task, receive_task)
            except:
                send_task.cancel()
                receive_task.cancel()
    except Exception as e:
        print("Megarip")
        return
            
if __name__ == "__main__":
    print("Welcome to The Chat Room")
    username = input("Username: ")
    
    asyncio.run(main(username))
            