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
        audio_data = await request.body()
        if not audio_data or len(audio_data) < 100:
            return Response(content="Audio too short", status_code=400)
            
        print(f"🎤 Received sound: {len(audio_data)} bytes")
        
        # رد زيزو الصافي
        reply_text = "يا خالد، أنا زيزو سامعك دلوقت بوضوح من غير وشوشة، هل الجهاز استقر عندك؟"
        
        communicate = edge_tts.Communicate(reply_text, "ar-EG-ShakirNeural")
        full_audio = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                full_audio += chunk["data"]
        
        return Response(content=full_audio, media_type="audio/mpeg")
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return Response(content=str(e), status_code=500)
