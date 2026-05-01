import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import google.generativeai as genai
import edge_tts
import io

app = FastAPI()

# مفتاح جيميناي بتاعك
genai.configure(api_key="AIzaSyAndb93kuF75k1zomXXI5zJFNpba-5bQSM")
model = genai.GenerativeModel('gemini-1.5-flash')

# صوت "شاكر" المجاني من إيدج
VOICE = "ar-EG-ShakirNeural" 

@app.get("/")
async def root():
    return {"message": "Zizo Server is Live"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Zizo Connected")
    try:
        while True:
            data = await websocket.receive()
            if "bytes" in data:
                # 1. جيميناي يولد الرد
                response = model.generate_content("رد باختصار جداً باللهجة السودانية كأنك صديق اسمه زيزو")
                reply_text = response.text
                print(f"Zizo says: {reply_text}")

                # 2. تحويل النص لصوت (Edge TTS المجاني)
                communicate = edge_tts.Communicate(reply_text, VOICE)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]

                # 3. إرسال الصوت للسماعة فوراً
                await websocket.send_bytes(audio_data)
                
    except Exception as e:
        print(f"Disconnected or Error: {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
