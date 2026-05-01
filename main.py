from fastapi import FastAPI, WebSocket
import uvicorn
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Zizo Server is Live!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("ESP32 Connected!")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            await websocket.send_text(f"Server received: {data}")
    except Exception as e:
        print(f"Disconnected: {e}")

if __name__ == "__main__":
    # رندر بيستخدم PORT متغير، لازم نقراه كدة
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
