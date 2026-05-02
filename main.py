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
    print("✅ Zizo is connected and stable!")
    try:
        while True:
            # استلام البيانات بمرونة أكبر لمنع الخطأ 1011
            data = await websocket.receive_bytes()
            if not data:
                continue
                
            print(f"🎤 Audio packet received: {len(data)} bytes")
            
            # الرد السريع لضمان بقاء الاتصال مفتوحاً
            reply_text = "زيزو سامعك يا خالد، جاري معالجة الصوت."
            
            communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    await websocket.send_bytes(chunk["data"])
            
            print("📤 Response sent back to ESP32")

    except WebSocketDisconnect:
        print("❌ Connection closed by user")
    except Exception as e:
        print(f"⚠️ Stable Mode Error: {e}")
