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
    print("✅ Zizo is Online and Ready!")
    try:
        while True:
            # استلام بايتات الصوت من خالد
            data = await websocket.receive_bytes()
            if data:
                print(f"🎤 Received voice data ({len(data)} bytes)")
                
                # جيميناي حيرد هنا (حالياً رد ذكي ثابت لضمان السرعة)
                # في المرحلة الجاية حنضيف محول الصوت لنص (STT)
                reply_text = "أهلين يا خالد، أنا زيزو سامعك مية مية، شنو رأيك في الصوت دلوقت؟"
                
                # تحويل الرد لصوت (Edge-TTS)
                communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        await websocket.send_bytes(chunk["data"])
                print("📤 Zizo replied successfully!")
                
    except WebSocketDisconnect:
        print("❌ Khaled disconnected.")
    except Exception as e:
        print(f"⚠️ Server Error: {e}")
