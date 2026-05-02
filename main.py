import os
from fastapi import FastAPI, Request, Response
import google.generativeai as genai
import edge_tts
import asyncio

app = FastAPI()

# إعداد جيميناي
genai.configure(api_key="AIzaSyAndb93kuF75k1zomXXI5zJFNpba-5bQSM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/talk")
async def talk_to_zizo(request: Request):
    try:
        # استلام البيانات كملف (Binary)
        audio_data = await request.body()
        if not audio_data:
            return Response(content="No data", status_code=400)
            
        print(f"🎤 Received voice data: {len(audio_data)} bytes")
        
        # رد زيزو (مرحلة التجربة الاستقرار)
        reply_text = "أهلين يا خالد، أنا زيزو سامعك دلوقت عبر نظام بوست المستقر. كيف الصوت عندك؟"
        
        # تحويل النص لصوت
        communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
        full_audio = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                full_audio += chunk["data"]
        
        print("📤 Sending audio response back to ESP32")
        return Response(content=full_audio, media_type="audio/mpeg")
        
    except Exception as e:
        print(f"⚠️ Server Error: {e}")
        return Response(content=str(e), status_code=500)

# نقطة فحص للسيرفر (اختياري)
@app.get("/")
async def root():
    return {"status": "Zizo Server is Live on POST mode"}
