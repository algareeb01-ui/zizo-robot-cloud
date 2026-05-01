import os
import asyncio
from fastapi import FastAPI, WebSocket
import google.generativeai as genai
import edge_tts

app = FastAPI()

# المفتاح ده خليه زي ما هو حالياً
genai.configure(api_key="AIzaSyAndb93kuF75k1zomXXI5zJFNpba-5bQSM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Zizo Connected!")
    try:
        while True:
            data = await websocket.receive_bytes()
            if data:
                print("🎤 Mic Received!")
                # رد سريع جداً
                reply_text = "أهلين يا خالد، أنا زيزو وسامعك كويس"
                
                communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        await websocket.send_bytes(chunk["data"])
                print("📤 Audio Sent!")
    except Exception as e:
        print(f"❌ Error: {e}")
