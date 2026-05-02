import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import google.generativeai as genai
import edge_tts

app = FastAPI()

genai.configure(api_key="AIzaSyAndb93kuF75k1zomXXI5zJFNpba-5bQSM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Zizo Link Established")
    try:
        while True:
            data = await websocket.receive_bytes()
            if data:
                # رد صوتي مباشر بدون نص لتجنب لخبطة السماعة
                text = "يا خالد أنا زيزو، سامعك مية مية والصوت دلوقت حيتحسن."
                communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
                
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        # إرسال الصوت كبايتات خام
                        await websocket.send_bytes(chunk["data"])
                print("📤 Audio Stream Sent")
    except Exception as e:
        print(f"⚠️ Connection Reset: {e}")
