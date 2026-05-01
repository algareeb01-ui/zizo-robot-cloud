import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import edge_tts

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Zizo connected and ready for voice!")
    try:
        while True:
            data = await websocket.receive_bytes()
            if data:
                print("🎤 Mic data received, sending voice reply...")
                
                # النص اللي حنحوله لصوت
                reply_text = "أهلين يا خالد، أنا زيزو سامعك وصوتك وصلني، جاري تشغيل الذكاء الاصطناعي"
                
                # تحويل النص لصوت (Audio Stream)
                communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        # إرسال بايتات الصوت للقطعة فوراً
                        await websocket.send_bytes(chunk["data"])
                print("📤 Voice sent!")
    except WebSocketDisconnect:
        print("❌ Disconnected")
    except Exception as e:
        print(f"🔥 Error: {e}")
