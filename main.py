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
    print("✅ Zizo Stable Connection")
    try:
        while True:
            # استلام البيانات بحجم أصغر لمنع الـ 1011
            data = await websocket.receive_bytes()
            if data:
                # رد صوتي مباشر ومضغوط
                text = "يا خالد، أنا زيزو. دلوقت الصوت حيكون أوضح بكتير."
                communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
                
                audio_buffer = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_buffer += chunk["data"]
                
                # إرسال الصوت على دفعات صغيرة للسماعة
                chunk_size = 1024
                for i in range(0, len(audio_buffer), chunk_size):
                    await websocket.send_bytes(audio_buffer[i:i + chunk_size])
                    await asyncio.sleep(0.01) # تنفس للسماعة
                
    except Exception as e:
        print(f"⚠️ Connection Status: {e}")
