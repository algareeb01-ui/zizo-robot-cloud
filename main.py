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
        # استلام ملف الصوت بالكامل
        audio_data = await request.body()
        print(f"🎤 Received voice file: {len(audio_data)} bytes")
        
        # حالياً رد ثابت سريع للتجربة (وفي الخطوة الجاية نربط STT)
        reply_text = "يا خالد، أنا زيزو. النظام ده ثابت دلوقت، هل سامعني بوضوح؟"
        
        # تحويل الرد لصوت
        communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
        full_audio = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                full_audio += chunk["data"]
        
        print("📤 Sending full response back...")
        return Response(content=full_audio, media_type="audio/mpeg")
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return Response(content="Error", status_code=500)
