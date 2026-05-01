import os
import asyncio
from fastapi import FastAPI, WebSocket
import google.generativeai as genai
import edge_tts

app = FastAPI()

# تأكد إن المفتاح ده صحيح
genai.configure(api_key="AIzaSyAndb93kuF75k1zomXXI5zJFNpba-5bQSM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Zizo connected and ready!")
    try:
        while True:
            data = await websocket.receive()
            if "bytes" in data:
                print("🎤 Received audio from Khaled...")
                
                # رد سريع ومباشر من جيميناي
                try:
                    response = model.generate_content("رد باختصار جداً باللهجة السودانية كأنك صديق اسمه زيزو")
                    reply_text = response.text
                    print(f"🤖 Zizo replied: {reply_text}")

                    # تحويل الرد لصوت
                    communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
                    audio_data = b""
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            audio_data += chunk["data"]

                    if audio_data:
                        await websocket.send_bytes(audio_data)
                        print("📤 Audio sent back to ESP32!")
                except Exception as e:
                    print(f"❌ Error in AI or TTS: {e}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
