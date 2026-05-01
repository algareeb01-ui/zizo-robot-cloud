import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Zizo connected!")
    try:
        while True:
            # استلام كـ بايتات (Bytes) حصراً
            data = await websocket.receive_bytes()
            if data:
                print(f"🎤 Received audio: {len(data)} bytes")
                # رد بسيط جداً (رسالة ترحيب ثابتة)
                # ملاحظة: هنا السيرفر حيرد عليك بنص كبداية
                await websocket.send_text("زيزو سامعك يا خالد، جاري معالجة الصوت")
    except WebSocketDisconnect:
        print("❌ Disconnected")
    except Exception as e:
        print(f"🔥 Server Error: {e}")
