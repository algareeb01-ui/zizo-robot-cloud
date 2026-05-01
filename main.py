import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import google.generativeai as genai
import edge_tts

app = FastAPI()

# تأكد إن المفتاح ده لسه شغال
genai.configure(api_key="AIzaSyAndb93kuF75k1zomXXI5zJFNpba-5bQSM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Zizo Connected and waiting for Khaled...")
    try:
        while True:
            # استلام البيانات كـ بايتات
            data = await websocket.receive_bytes()
            if data:
                print(f"🎤 Received {len(data)} bytes of audio data")
                
                try:
                    # رد تجريبي ثابت لكسر العطل
                    reply_text = "أهلين يا خالد، أنا زيزو سامعك"
                    print(f"🤖 Replying: {reply_text}")

                    communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
                    audio_out = b""
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            audio_out += chunk["data"]
                    
                    if audio_out:
                        await websocket.send_bytes(audio_out)
                        print("📤 Audio response sent back successfully!")
                
                except Exception as ai_err:
                    print(f"❌ AI/TTS Error: {ai_err}")

    except WebSocketDisconnect:
        print("❌ Khaled disconnected.")
    except Exception as e:
        print(f"❌ Critical Server Error: {e}")
