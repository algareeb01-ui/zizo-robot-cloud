import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import google.generativeai as genai
import edge_tts

app = FastAPI()

# إعداد جيميناي
genai.configure(api_key="AIzaSyAndb93kuF75k1zomXXI5zJFNpba-5bQSM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Connection Stable")
    try:
        while True:
            # استلام البيانات
            data = await websocket.receive_bytes()
            if len(data) > 0:
                print(f"🎤 Received chunk: {len(data)} bytes")
                
                # رد سريع ومختصر لتقليل الضغط
                reply_text = "أهلاً خالد، أنا سامعك."
                
                communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
                # تجميع الصوت وإرساله قطعة واحدة كبيرة
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                
                if audio_data:
                    await websocket.send_bytes(audio_data)
                    print("📤 Full Audio Sent")
                    
    except Exception as e:
        print(f"⚠️ Socket Info: {e}")
