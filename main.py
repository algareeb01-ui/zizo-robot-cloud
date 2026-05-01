import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import google.generativeai as genai
import edge_tts

app = FastAPI()

# مفتاح جيميناي بتاعك
genai.configure(api_key="AIzaSyAndb93kuF75k1zomXXI5zJFNpba-5bQSM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Zizo is Ready!")
    try:
        while True:
            data = await websocket.receive_bytes()
            if data:
                # هنا السيرفر حيفترض إن البيانات دي هي صوتك (نحولها لنص مستقبلاً)
                # حالياً حنخلي جيميناي يرد برد ذكي بناءً على نبضة الصوت
                print("🎤 Mic data received...")
                
                # طلب رد من جيميناي
                prompt = "رد كأنك صديق سوداني اسمه زيزو، رحب بخالد وقول ليه أنا سامعك كويس"
                response = model.generate_content(prompt)
                reply_text = response.text
                print(f"🤖 Zizo says: {reply_text}")

                # تحويل النص لصوت شاکر (المصري/السوداني القريب)
                communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        await websocket.send_bytes(chunk["data"])
                print("📤 Voice reply sent!")
    except Exception as e:
        print(f"⚠️ Error: {e}")
